import { useState } from "react"
import useAlerts from "../hooks/useAlerts"
import useStore from "../store/useStore"

const RISK_COLORS = {
  high: "bg-red-100 text-red-800",
  medium: "bg-yellow-100 text-yellow-800",
  low: "bg-green-100 text-green-800",
}

function getRiskLevel(score) {
  if (score >= 0.6) return "high"
  if (score >= 0.3) return "medium"
  return "low"
}

function AlertCard({ alert }) {
  const risk = getRiskLevel(alert.risk_score)
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4 mb-3 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <span className={"text-xs font-semibold px-2 py-1 rounded-full " + RISK_COLORS[risk]}>
          {risk.toUpperCase()} RISK
        </span>
        <span className="text-xs text-gray-400">{alert.source_forum}</span>
      </div>
      <p className="text-sm text-gray-700 mb-2 line-clamp-3">{alert.post_text}</p>
      <div className="flex flex-wrap gap-1 mb-2">
        {alert.keywords.slice(0, 5).map((kw) => (
          <span key={kw} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
            {kw}
          </span>
        ))}
      </div>
      <div className="flex justify-between text-xs text-gray-400">
        <span>Type: {alert.threat_type.replace("_", " ")}</span>
        <span>Score: {(alert.risk_score * 100).toFixed(0)}%</span>
        {alert.is_anomaly && (
          <span className="text-purple-600 font-semibold">Anomaly</span>
        )}
      </div>
    </div>
  )
}

function AlertFeed() {
  const [minRisk, setMinRisk] = useState(0.0)
  const [threatType, setThreatType] = useState(null)
  const alerts = useAlerts(50, minRisk, threatType)
  const loading = useStore((s) => s.loading)
  const error = useStore((s) => s.error)

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Alert Feed</h1>
      <p className="text-gray-500 text-sm mb-6">Live threat posts ranked by risk score</p>

      <div className="flex gap-4 mb-6 flex-wrap">
        <div>
          <label className="text-xs text-gray-500 block mb-1">Min risk score</label>
          <select
            className="border border-gray-200 rounded-lg px-3 py-2 text-sm"
            onChange={(e) => setMinRisk(parseFloat(e.target.value))}
          >
            <option value="0.0">All</option>
            <option value="0.3">Medium+</option>
            <option value="0.6">High only</option>
          </select>
        </div>
        <div>
          <label className="text-xs text-gray-500 block mb-1">Threat type</label>
          <select
            className="border border-gray-200 rounded-lg px-3 py-2 text-sm"
            onChange={(e) => setThreatType(e.target.value || null)}
          >
            <option value="">All types</option>
            <option value="credential_leak">Credential leak</option>
            <option value="ransomware">Ransomware</option>
            <option value="zero_day">Zero day</option>
            <option value="malware_sale">Malware sale</option>
          </select>
        </div>
      </div>

      {loading && <p className="text-gray-400 text-sm">Loading alerts...</p>}
      {error && <p className="text-red-500 text-sm">Error: {error}</p>}
      {!loading && alerts.length === 0 && (
        <p className="text-gray-400 text-sm">No alerts found.</p>
      )}
      {alerts.map((alert) => (
        <AlertCard key={alert.id} alert={alert} />
      ))}
    </div>
  )
}

export default AlertFeed