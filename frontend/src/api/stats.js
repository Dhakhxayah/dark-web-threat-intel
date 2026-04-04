import client from "./client"

export function fetchClassifierStats() {
  return client.get("/api/v1/stats/classifier")
}

export function fetchPipelineSummary() {
  return client.get("/api/v1/stats/pipeline")
}