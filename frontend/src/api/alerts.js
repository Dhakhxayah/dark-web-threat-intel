import client from "./client"

export function fetchAlerts(limit = 50, minRisk = 0.0, threatType = null) {
  const params = { limit, min_risk: minRisk }
  if (threatType) params.threat_type = threatType
  return client.get("/api/v1/alerts/", { params })
}

export function fetchAnomalyAlerts(limit = 50) {
  return client.get("/api/v1/alerts/anomalies", { params: { limit } })
}

export function analyzeText(text) {
  return client.post("/api/v1/alerts/analyze", { text })
}