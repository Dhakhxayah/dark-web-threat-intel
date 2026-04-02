import os
import uuid
import pandas as pd
from fastapi import APIRouter, HTTPException
from app.core.logger import get_logger
from app.core.config import get_settings
from pipeline.classifier import load_classifier, predict_threat_type
from pipeline.anomaly import load_anomaly_model, predict_anomaly
from pipeline.preprocess import compute_risk_score

logger = get_logger(__name__)
settings = get_settings()
router = APIRouter()

clf = None
clf_vectorizer = None
anomaly_model = None
anomaly_vectorizer = None


def load_models():
    global clf, clf_vectorizer, anomaly_model, anomaly_vectorizer
    try:
        clf, clf_vectorizer = load_classifier("data/models/classifier")
        anomaly_model, anomaly_vectorizer = load_anomaly_model("data/models/anomaly")
        logger.info("Alert models loaded successfully")
    except Exception as e:
        logger.info("Models not found, will use rule-based fallback: " + str(e))


load_models()


def build_alert_from_row(row):
    keywords = str(row.get("keywords", "")).split(",")
    keywords = [k.strip() for k in keywords if k.strip() != ""]
    is_anomaly = bool(row.get("is_anomaly", False))
    risk_score = float(row.get("risk_score", compute_risk_score(keywords, is_anomaly)))

    return {
        "id": str(row.get("id", uuid.uuid4())),
        "post_text": str(row.get("cleaned_text", ""))[:300],
        "threat_type": str(row.get("threat_type", "unknown")),
        "risk_score": risk_score,
        "is_anomaly": is_anomaly,
        "source_forum": str(row.get("source_forum", "unknown")),
        "timestamp": str(row.get("timestamp", "")),
        "keywords": keywords,
    }


@router.get("/")
def get_alerts(limit = 50, min_risk = 0.0, threat_type = None):
    try:
        data_path = os.path.join(settings.data_processed_path, "clean_posts.csv")
        df = pd.read_csv(data_path)
        df = df.dropna(subset=["cleaned_text"])

        if threat_type:
            df = df[df["threat_type"] == threat_type]

        if "risk_score" in df.columns:
            df = df[df["risk_score"] >= min_risk]
            df = df.sort_values("risk_score", ascending=False)

        df = df.head(limit)
        alerts = [build_alert_from_row(row) for _, row in df.iterrows()]
        return {"total": len(alerts), "alerts": alerts}

    except Exception as e:
        logger.info("Error fetching alerts: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load alerts")


@router.get("/anomalies")
def get_anomalies(limit = 50):
    try:
        data_path = os.path.join(settings.data_processed_path, "clean_posts.csv")
        df = pd.read_csv(data_path)
        df = df.dropna(subset=["cleaned_text"])

        if "is_anomaly" in df.columns:
            df = df[df["is_anomaly"] == True]

        df = df.head(limit)
        alerts = [build_alert_from_row(row) for _, row in df.iterrows()]
        return {"total": len(alerts), "anomalies": alerts}

    except Exception as e:
        logger.info("Error fetching anomalies: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load anomalies")


@router.post("/analyze")
def analyze_text(payload: dict):
    try:
        text = payload.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="text field is required")

        threat_type = "unknown"
        confidence = 0.0
        is_anomaly = False
        anomaly_score = 0.0

        if clf and clf_vectorizer:
            threat_type, confidence = predict_threat_type(clf, clf_vectorizer, text)

        if anomaly_model and anomaly_vectorizer:
            is_anomaly, anomaly_score = predict_anomaly(anomaly_model, anomaly_vectorizer, text)

        from pipeline.preprocess import extract_keywords, compute_risk_score, clean_text
        cleaned = clean_text(text)
        keywords = extract_keywords(cleaned)
        risk_score = compute_risk_score(keywords, is_anomaly)

        return {
            "threat_type": threat_type,
            "confidence": confidence,
            "is_anomaly": is_anomaly,
            "anomaly_score": anomaly_score,
            "keywords": keywords,
            "risk_score": risk_score,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.info("Error analyzing text: " + str(e))
        raise HTTPException(status_code=500, detail="Analysis failed")