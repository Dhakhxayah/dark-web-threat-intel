from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ThreatAlert(BaseModel):
    id: str = ""
    post_text: str = ""
    threat_type: str = "unknown"
    risk_score: float = 0.0
    is_anomaly: bool = False
    source_forum: str = ""
    timestamp: str = ""
    keywords: List[str] = []

    def to_dict(self):
        return {
            "id": self.id,
            "post_text": self.post_text,
            "threat_type": self.threat_type,
            "risk_score": self.risk_score,
            "is_anomaly": self.is_anomaly,
            "source_forum": self.source_forum,
            "timestamp": self.timestamp,
            "keywords": self.keywords,
        }


class TopicSummary(BaseModel):
    topic_id: int = 0
    label: str = ""
    top_words: List[str] = []
    weight: float = 0.0

    def to_dict(self):
        return {
            "topic_id": self.topic_id,
            "label": self.label,
            "top_words": self.top_words,
            "weight": self.weight,
        }


class GraphNode(BaseModel):
    id: str = ""
    label: str = ""
    node_type: str = "keyword"
    degree: int = 0

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "node_type": self.node_type,
            "degree": self.degree,
        }


class GraphEdge(BaseModel):
    source: str = ""
    target: str = ""
    weight: float = 1.0

    def to_dict(self):
        return {
            "source": self.source,
            "target": self.target,
            "weight": self.weight,
        }