from pydantic import BaseModel
from datetime import datetime

class ThreatAlert(BaseModel):
    id = ""
    post_text = ""
    threat_type = "unknown" 
    risk_score = 0.0 
    is_anomaly = False 
    source_forum = "" 
    timestamp = None 
    keywords = []

class TopicSummary(BaseModel):
    topic_id = 0 
    label = "" 
    top_words = [] 
    weight = 0.0 

class GraphNode(BaseModel):
    id = ""
    label = ""
    node_type = "keyword" 
    degree = 0 

class GraphEdge(BaseModel):
    source = ""
    target = "" 
    weight = 1.0
    
    