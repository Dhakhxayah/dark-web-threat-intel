import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.models.threat import ThreatAlert, TopicSummary, GraphNode, GraphEdge


def test_threat_alert_to_dict():
    alert = ThreatAlert(
        id="abc123",
        post_text="ransomware for sale",
        threat_type="ransomware",
        risk_score=0.8,
        is_anomaly=True,
        source_forum="breach_forum",
        timestamp="2024-01-01",
        keywords=["ransomware"],
    )
    d = alert.to_dict()
    assert d["id"] == "abc123"
    assert d["threat_type"] == "ransomware"
    assert d["risk_score"] == 0.8
    assert d["is_anomaly"] == True
    assert "ransomware" in d["keywords"]


def test_topic_summary_to_dict():
    topic = TopicSummary(
        topic_id=1,
        label="Ransomware campaigns",
        top_words=["ransom", "encrypt", "bitcoin"],
        weight=0.15,
    )
    d = topic.to_dict()
    assert d["topic_id"] == 1
    assert d["label"] == "Ransomware campaigns"
    assert "ransom" in d["top_words"]


def test_graph_node_to_dict():
    node = GraphNode(
        id="breach_forum",
        label="breach_forum",
        node_type="actor",
        degree=12,
    )
    d = node.to_dict()
    assert d["node_type"] == "actor"
    assert d["degree"] == 12


def test_graph_edge_to_dict():
    edge = GraphEdge(
        source="breach_forum",
        target="ransomware",
        weight=5.0,
    )
    d = edge.to_dict()
    assert d["source"] == "breach_forum"
    assert d["target"] == "ransomware"
    assert d["weight"] == 5.0


def test_default_risk_score():
    alert = ThreatAlert(
        id="x",
        post_text="hello",
        threat_type="unknown",
        risk_score=0.0,
        is_anomaly=False,
        source_forum="unknown",
        timestamp="2024-01-01",
        keywords=[],
    )
    assert alert.risk_score == 0.0


def test_graph_node_default_degree():
    node = GraphNode(
        id="test",
        label="test",
        node_type="keyword",
    )
    assert node.degree == 0