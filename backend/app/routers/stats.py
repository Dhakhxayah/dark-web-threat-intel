import os
import json
from fastapi import APIRouter, HTTPException
from app.core.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/classifier")
def get_classifier_stats():
    try:
        report_path = "data/models/classifier/classifier_report.json"
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="Classifier report not found. Run the pipeline first.")
        with open(report_path, "r") as f:
            report = json.load(f)
        return report
    except HTTPException:
        raise
    except Exception as e:
        logger.info("Error loading classifier stats: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load classifier stats")


@router.get("/pipeline")
def get_pipeline_summary():
    try:
        summary = {
            "steps": [
                {"name": "NLP preprocessing", "tool": "spaCy + NLTK",          "status": "complete"},
                {"name": "Topic modeling",     "tool": "LDA — 10 topics",       "status": "complete"},
                {"name": "Classification",     "tool": "Random Forest + TF-IDF","status": "complete"},
                {"name": "Anomaly detection",  "tool": "Isolation Forest",       "status": "complete"},
                {"name": "Graph analysis",     "tool": "networkx",               "status": "complete"},
            ]
        }
        return summary
    except Exception as e:
        logger.info("Error loading pipeline summary: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load pipeline summary")