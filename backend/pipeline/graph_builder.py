import os
import json
import pandas as pd
import networkx as nx
from app.core.logger import get_logger

logger = get_logger(__name__)

THREAT_KEYWORDS = [
    "ransomware", "malware", "exploit", "zero-day", "credential",
    "leak", "breach", "dump", "botnet", "phishing", "trojan",
    "backdoor", "keylogger", "ddos", "vulnerability", "cve",
    "stealer", "rat", "c2", "bitcoin", "monero", "ransom"
]


def build_graph(df):
    logger.info("Building threat network graph...")
    G = nx.Graph()

    for _, row in df.iterrows():
        keywords_str = str(row.get("keywords", ""))
        threat_type = str(row.get("threat_type", "unknown"))
        source_forum = str(row.get("source_forum", "unknown"))

        if keywords_str.strip() == "" or keywords_str == "nan":
            continue

        keywords = [k.strip() for k in keywords_str.split(",") if k.strip() != ""]

        if source_forum and source_forum != "nan":
            if not G.has_node(source_forum):
                G.add_node(source_forum, node_type="actor")

        if threat_type and threat_type != "nan" and threat_type != "unknown":
            if not G.has_node(threat_type):
                G.add_node(threat_type, node_type="attack_type")

        for keyword in keywords:
            if not G.has_node(keyword):
                G.add_node(keyword, node_type="keyword")

            if source_forum and source_forum != "nan":
                if G.has_edge(source_forum, keyword):
                    G[source_forum][keyword]["weight"] += 1
                else:
                    G.add_edge(source_forum, keyword, weight=1)

            if threat_type and threat_type != "unknown" and threat_type != "nan":
                if G.has_edge(keyword, threat_type):
                    G[keyword][threat_type]["weight"] += 1
                else:
                    G.add_edge(keyword, threat_type, weight=1)

    logger.info("Graph built with " + str(G.number_of_nodes()) + " nodes and " + str(G.number_of_edges()) + " edges")
    return G


def get_graph_stats(G):
    stats = {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "top_connected_nodes": [],
    }
    degree_list = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    for node, degree in degree_list[:10]:
        stats["top_connected_nodes"].append({
            "node": node,
            "degree": degree,
            "node_type": G.nodes[node].get("node_type", "unknown"),
        })
    return stats


def graph_to_dict(G):
    nodes = []
    for node_id, data in G.nodes(data=True):
        nodes.append({
            "id": node_id,
            "label": node_id,
            "node_type": data.get("node_type", "keyword"),
            "degree": G.degree(node_id),
        })

    edges = []
    for source, target, data in G.edges(data=True):
        edges.append({
            "source": source,
            "target": target,
            "weight": data.get("weight", 1),
        })

    return {"nodes": nodes, "edges": edges}


def save_graph(G, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    graph_dict = graph_to_dict(G)
    output_path = os.path.join(output_dir, "threat_graph.json")
    with open(output_path, "w") as f:
        json.dump(graph_dict, f, indent=2)
    logger.info("Saved graph to " + output_path)


def load_graph(output_dir):
    graph_path = os.path.join(output_dir, "threat_graph.json")
    with open(graph_path, "r") as f:
        graph_dict = json.load(f)
    logger.info("Loaded graph from " + graph_path)
    return graph_dict


def run_graph_builder(cleaned_data_path, output_dir):
    df = pd.read_csv(cleaned_data_path)
    df = df.dropna(subset=["cleaned_text"])
    G = build_graph(df)
    stats = get_graph_stats(G)
    logger.info("Graph stats: " + str(stats))
    save_graph(G, output_dir)
    return G, graph_to_dict(G)


if __name__ == "__main__":
    run_graph_builder(
        cleaned_data_path="data/processed/clean_posts.csv",
        output_dir="data/models/graph"
    )