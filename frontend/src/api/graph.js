import client from "./client"

export function fetchFullGraph() {
  return client.get("/api/v1/graph/")
}

export function fetchGraphNodes(nodeType = null) {
  const params = {}
  if (nodeType) params.node_type = nodeType
  return client.get("/api/v1/graph/nodes", { params })
}

export function fetchNodeConnections(nodeId) {
  return client.get("/api/v1/graph/node/" + nodeId)
}

export function fetchGraphStats() {
  return client.get("/api/v1/graph/stats")
}