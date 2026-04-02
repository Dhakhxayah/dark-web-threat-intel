import client from "./client"

export function fetchAnomalies(limit = 50) {
  return client.get("/api/v1/anomalies/", { params: { limit } })
}

export function fetchAnomalyTimeline() {
  return client.get("/api/v1/anomalies/timeline")
}

export function fetchAnomalyStats() {
  return client.get("/api/v1/anomalies/stats")
}