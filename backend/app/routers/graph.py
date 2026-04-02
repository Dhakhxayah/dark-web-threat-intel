import os
from fastapi import APIRouter, HTTPException
from app.core.logger import get_logger
from pipeline.graph_builder import load_graph

logger = get_logger(__name__)
router = APIRouter()

GRAPH_PATH = "data/models/graph"


@router.get("/")
def get_full_graph():
    try:
        graph_dict = load_graph(GRAPH_PATH)
        return {
            "total_nodes": len(graph_dict["nodes"]),
            "total_edges": len(graph_dict["edges"]),
            "graph": graph_dict,
        }
    except Exception as e:
        logger.info("Error loading graph: " + str(e))
        raise HTTPException(status_code=500, detail="Graph not built yet")


@router.get("/nodes")
def get_nodes(node_type = None):
    try:
        graph_dict = load_graph(GRAPH_PATH)
        nodes = graph_dict["nodes"]

        if node_type:
            nodes = [n for n in nodes if n["node_type"] == node_type]

        nodes = sorted(nodes, key=lambda x: x["degree"], reverse=True)
        return {"total": len(nodes), "nodes": nodes}

    except Exception as e:
        logger.info("Error loading nodes: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load nodes")


@router.get("/node/{node_id}")
def get_node_connections(node_id):
    try:
        graph_dict = load_graph(GRAPH_PATH)
        edges = graph_dict["edges"]

        connected_edges = [
            e for e in edges
            if e["source"] == node_id or e["target"] == node_id
        ]

        connected_node_ids = set()
        for e in connected_edges:
            connected_node_ids.add(e["source"])
            connected_node_ids.add(e["target"])

        connected_nodes = [
            n for n in graph_dict["nodes"]
            if n["id"] in connected_node_ids
        ]

        return {
            "node_id": node_id,
            "total_connections": len(connected_edges),
            "connected_nodes": connected_nodes,
            "edges": connected_edges,
        }

    except Exception as e:
        logger.info("Error loading node connections: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load node data")


@router.get("/stats")
def get_graph_stats():
    try:
        graph_dict = load_graph(GRAPH_PATH)
        nodes = graph_dict["nodes"]
        edges = graph_dict["edges"]

        actor_count = len([n for n in nodes if n["node_type"] == "actor"])
        keyword_count = len([n for n in nodes if n["node_type"] == "keyword"])
        attack_count = len([n for n in nodes if n["node_type"] == "attack_type"])

        top_nodes = sorted(nodes, key=lambda x: x["degree"], reverse=True)[:5]

        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "actor_nodes": actor_count,
            "keyword_nodes": keyword_count,
            "attack_type_nodes": attack_count,
            "top_connected_nodes": top_nodes,
        }

    except Exception as e:
        logger.info("Error fetching graph stats: " + str(e))
        raise HTTPException(status_code=500, detail="Failed to load graph stats")