import os
import json
import pandas as pd
from fastapi import APIRouter, HTTPException
from app.core.logger import get_logger
from app.core.config import get_settings
from pipeline.topic_model import load_model, get_topic_summary

logger = get_logger(__name__)
settings = get_settings()
router = APIRouter()

lda_model = None
lda_dictionary = None


def load_topic_model():
    global lda_model, lda_dictionary
    try:
        lda_model, lda_dictionary = load_model("data/models/lda")
        logger.info("LDA model loaded successfully")
    except Exception as e:
        logger.info("LDA model not found: " + str(e))


load_topic_model()


@router.get("/")
def get_topics():
    try:
        if lda_model is None:
            return {"topics": [], "message": "Model not trained yet"}

        summaries = get_topic_summary(lda_model)
        return {"total": len(summaries), "topics": summaries}

    except Exception as e:
        logger.info("Error fetching topics: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load topics")


@router.get("/trending")
def get_trending_topics():
    try:
        data_path = os.path.join(settings.data_processed_path, "clean_posts.csv")
        df = pd.read_csv(data_path)
        df = df.dropna(subset=["cleaned_text"])

        if "dominant_topic" not in df.columns:
            return {"trending": [], "message": "Topic assignment not done yet"}

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.dropna(subset=["timestamp"])
            df = df.sort_values("timestamp", ascending=False)
            recent = df.head(int(len(df) * 0.2))
        else:
            recent = df.head(200)

        topic_counts = recent["dominant_topic"].value_counts().reset_index()
        topic_counts.columns = ["topic_id", "post_count"]

        if lda_model:
            summaries = get_topic_summary(lda_model)
            label_map = {s["topic_id"]: s["label"] for s in summaries}
            words_map = {s["topic_id"]: s["top_words"] for s in summaries}
        else:
            label_map = {}
            words_map = {}

        trending = []
        for _, row in topic_counts.iterrows():
            topic_id = int(row["topic_id"])
            trending.append({
                "topic_id": topic_id,
                "label": label_map.get(topic_id, "Topic " + str(topic_id)),
                "post_count": int(row["post_count"]),
                "top_words": words_map.get(topic_id, []),
            })

        return {"total": len(trending), "trending": trending}

    except Exception as e:
        logger.info("Error fetching trending topics: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load trending topics")


@router.get("/{topic_id}")
def get_topic_posts(topic_id, limit = 20):
    try:
        topic_id = int(topic_id)
        data_path = os.path.join(settings.data_processed_path, "clean_posts.csv")
        df = pd.read_csv(data_path)
        df = df.dropna(subset=["cleaned_text"])

        if "dominant_topic" not in df.columns:
            return {"posts": [], "message": "Topic assignment not done yet"}

        topic_df = df[df["dominant_topic"] == topic_id].head(limit)
        posts = topic_df[["cleaned_text", "source_forum", "timestamp"]].to_dict(orient="records")
        return {"topic_id": topic_id, "total": len(posts), "posts": posts}

    except Exception as e:
        logger.info("Error fetching topic posts: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load topic posts")