import { useState, useEffect } from "react"
import { fetchClassifierStats, fetchPipelineSummary } from "../api/stats"
import client from "../api/client"

function StatCard({ label, value, color, subtitle }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4">
      <p className="text-xs text-gray-400 mb-1">{label}</p>
      <p className={"text-2xl font-bold " + (color || "text-gray-800")}>{value ?? "—"}</p>
      {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
    </div>
  )
}

function MetricBar({ label, value, color }) {
  return (
    <div className="mb-3">
      <div className="flex justify-between text-xs text-gray-500 mb-1">
        <span>{label}</span>
        <span className="font-semibold">{(value * 100).toFixed(1)}%</span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-2">
        <div className={"h-2 rounded-full " + color} style={{ width: (value * 100) + "%" }}></div>
      </div>
    </div>
  )
}

const CLASS_COLORS = {
  credential_leak: "bg-blue-500",
  malware_sale:    "bg-purple-500",
  ransomware:      "bg-red-500",
  zero_day:        "bg-amber-500",
  unknown:         "bg-gray-400",
}

function ModelStats() {
  const [classifierStats, setClassifierStats] = useState(null)
  const [anomalyStats, setAnomalyStats]       = useState(null)
  const [graphStats, setGraphStats]           = useState(null)
  const [pipeline, setPipeline]               = useState([])
  const [loading, setLoading]                 = useState(true)

  useEffect(() => {
    Promise.all([
      fetchClassifierStats().then((r) => setClassifierStats(r.data)),
      fetchPipelineSummary().then((r) => setPipeline(r.data.steps || [])),
      client.get("/api/v1/anomalies/stats").then((r) => setAnomalyStats(r.data)),
      client.get("/api/v1/graph/stats").then((r) => setGraphStats(r.data)),
    ])
      .catch((err) => console.error("Stats error:", err))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="p-6 text-gray-400">Loading model stats...</p>

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Model Performance</h1>
      <p className="text-gray-500 text-sm mb-6">Live ML pipeline accuracy and system statistics</p>

      {classifierStats && (
        <>
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
            Classifier — Random Forest
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <StatCard label="Overall accuracy" value={(classifierStats.accuracy * 100).toFixed(1) + "%"}                   color="text-green-600" subtitle="on test set" />
            <StatCard label="Macro precision"  value={(classifierStats.macro_avg.precision * 100).toFixed(1) + "%"}         color="text-blue-600" />
            <StatCard label="Macro recall"     value={(classifierStats.macro_avg.recall * 100).toFixed(1) + "%"}            color="text-indigo-600" />
            <StatCard label="Macro F1 score"   value={(classifierStats.macro_avg.f1 * 100).toFixed(1) + "%"}               color="text-purple-600" />
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6">
            <h2 className="text-sm font-semibold text-gray-600 mb-4">Per-class performance</h2>
            {classifierStats.classes.map((cls) => (
              <div key={cls.name} className="mb-4">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm font-medium text-gray-700">{cls.name.replace("_", " ")}</span>
                  <span className="text-xs text-gray-400">{cls.support} samples</span>
                </div>
                <MetricBar label="Precision" value={cls.precision} color={CLASS_COLORS[cls.name] || "bg-gray-500"} />
                <MetricBar label="Recall"    value={cls.recall}    color={CLASS_COLORS[cls.name] || "bg-gray-500"} />
                <MetricBar label="F1 score"  value={cls.f1}        color={CLASS_COLORS[cls.name] || "bg-gray-500"} />
              </div>
            ))}
          </div>
        </>
      )}

      {anomalyStats && (
        <>
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
            Anomaly Detection — Isolation Forest
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <StatCard label="Total posts"     value={anomalyStats.total_posts}              color="text-gray-800" />
            <StatCard label="Anomalies found" value={anomalyStats.anomaly_count}            color="text-red-500" />
            <StatCard label="Normal posts"    value={anomalyStats.normal_count}             color="text-green-600" />
            <StatCard label="Anomaly rate"    value={anomalyStats.anomaly_rate_percent + "%"} color="text-amber-500" />
          </div>
        </>
      )}

      {graphStats && (
        <>
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
            Network Graph — networkx
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <StatCard label="Total nodes"   value={graphStats.total_nodes}       color="text-gray-800" />
            <StatCard label="Total edges"   value={graphStats.total_edges}       color="text-gray-800" />
            <StatCard label="Threat actors" value={graphStats.actor_nodes}       color="text-blue-600" />
            <StatCard label="Attack types"  value={graphStats.attack_type_nodes} color="text-red-500" />
          </div>
        </>
      )}

      {pipeline.length > 0 && (
        <>
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
            Pipeline summary
          </h2>
          <div className="bg-white rounded-xl border border-gray-200 p-4">
            <div className="space-y-2 text-sm text-gray-600">
              {pipeline.map((step) => (
                <div key={step.name} className="flex justify-between py-2 border-b border-gray-100 last:border-0">
                  <span>{step.name}</span>
                  <span className="text-green-600 font-medium">{step.tool}</span>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default ModelStats