import os
import pandas as pd
from fastapi import APIRouter, HTTPException
from app.core.logger import get_logger
from app.core.config import get_settings

logger = get_logger(__name__)
settings = get_settings()
router = APIRouter()


@router.get("/")
def get_anomalies(limit = 50):
    try:
        data_path = os.path.join(settings.data_processed_path, "clean_posts.csv")
        df = pd.read_csv(data_path)
        df = df.dropna(subset=["cleaned_text"])

        if "is_anomaly" not in df.columns:
            return {"anomalies": [], "message": "Anomaly detection not run yet"}

        anomalies = df[df["is_anomaly"] == True].copy()

        if "anomaly_score" in anomalies.columns:
            anomalies = anomalies.sort_values("anomaly_score")

        anomalies = anomalies.head(limit)

        result = []
        for _, row in anomalies.iterrows():
            result.append({
                "post_text": str(row.get("cleaned_text", ""))[:300],
                "anomaly_score": float(row.get("anomaly_score", 0.0)),
                "source_forum": str(row.get("source_forum", "unknown")),
                "timestamp": str(row.get("timestamp", "")),
                "keywords": str(row.get("keywords", "")).split(","),
            })

        return {"total": len(result), "anomalies": result}

    except Exception as e:
        logger.info("Error fetching anomalies: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load anomalies")


@router.get("/timeline")
def get_anomaly_timeline():
    try:
        data_path = os.path.join(settings.data_processed_path, "clean_posts.csv")
        df = pd.read_csv(data_path)
        df = df.dropna(subset=["cleaned_text"])

        if "is_anomaly" not in df.columns or "timestamp" not in df.columns:
            return {"timeline": [], "message": "Required columns missing"}

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
        df["date"] = df["timestamp"].dt.date

        timeline = df.groupby("date").agg(
            total_posts=("cleaned_text", "count"),
            anomaly_count=("is_anomaly", "sum")
        ).reset_index()

        timeline["date"] = timeline["date"].astype(str)
        result = timeline.to_dict(orient="records")

        return {"total_days": len(result), "timeline": result}

    except Exception as e:
        logger.info("Error building anomaly timeline: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to build timeline")


@router.get("/stats")
def get_anomaly_stats():
    try:
        data_path = os.path.join(settings.data_processed_path, "clean_posts.csv")
        df = pd.read_csv(data_path)

        if "is_anomaly" not in df.columns:
            return {"message": "Anomaly detection not run yet"}

        total = len(df)
        anomaly_count = int(df["is_anomaly"].sum())
        normal_count = total - anomaly_count
        anomaly_rate = round(anomaly_count / total * 100, 2) if total > 0 else 0

        return {
            "total_posts": total,
            "anomaly_count": anomaly_count,
            "normal_count": normal_count,
            "anomaly_rate_percent": anomaly_rate,
        }

    except Exception as e:
        logger.info("Error fetching anomaly stats: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load stats")