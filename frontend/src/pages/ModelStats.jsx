import { useState, useEffect } from "react"
import { fetchGraphStats } from "../api/graph"
import client from "../api/client"

function StatCard({ label, value, color, subtitle }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4">
      <p className="text-xs text-gray-400 mb-1">{label}</p>
      <p className={"text-2xl font-bold " + (color || "text-gray-800")}>{value}</p>
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
        <div
          className={"h-2 rounded-full " + color}
          style={{ width: (value * 100) + "%" }}
        ></div>
      </div>
    </div>
  )
}

const CLASSIFIER_STATS = {
  accuracy: 1.0,
  macro_avg: { precision: 1.0, recall: 1.0, f1: 1.0 },
  weighted_avg: { precision: 1.0, recall: 1.0, f1: 1.0 },
  classes: [
    { name: "credential_leak", precision: 1.0, recall: 1.0, f1: 1.0, support: 74 },
    { name: "malware_sale",    precision: 1.0, recall: 1.0, f1: 1.0, support: 68 },
    { name: "ransomware",      precision: 1.0, recall: 1.0, f1: 1.0, support: 37 },
    { name: "zero_day",        precision: 1.0, recall: 1.0, f1: 1.0, support: 37 },
    { name: "unknown",         precision: 1.0, recall: 1.0, f1: 1.0, support: 181 },
  ],
}

const CLASS_COLORS = {
  credential_leak: "bg-blue-500",
  malware_sale:    "bg-purple-500",
  ransomware:      "bg-red-500",
  zero_day:        "bg-amber-500",
  unknown:         "bg-gray-400",
}

function ModelStats() {
  const [graphStats, setGraphStats] = useState(null)
  const [anomalyStats, setAnomalyStats] = useState(null)

  useEffect(() => {
    client.get("/api/v1/graph/stats")
      .then((res) => setGraphStats(res.data))
      .catch((err) => console.error(err))

    client.get("/api/v1/anomalies/stats")
      .then((res) => setAnomalyStats(res.data))
      .catch((err) => console.error(err))
  }, [])

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Model Performance</h1>
      <p className="text-gray-500 text-sm mb-6">ML pipeline accuracy and system statistics</p>

      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Classifier — Random Forest</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <StatCard label="Overall accuracy"   value={(CLASSIFIER_STATS.accuracy * 100).toFixed(1) + "%"}          color="text-green-600" subtitle="on test set" />
        <StatCard label="Macro precision"    value={(CLASSIFIER_STATS.macro_avg.precision * 100).toFixed(1) + "%"} color="text-blue-600" />
        <StatCard label="Macro recall"       value={(CLASSIFIER_STATS.macro_avg.recall * 100).toFixed(1) + "%"}    color="text-indigo-600" />
        <StatCard label="Macro F1 score"     value={(CLASSIFIER_STATS.macro_avg.f1 * 100).toFixed(1) + "%"}        color="text-purple-600" />
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6">
        <h2 className="text-sm font-semibold text-gray-600 mb-4">Per-class performance</h2>
        {CLASSIFIER_STATS.classes.map((cls) => (
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

      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Anomaly Detection — Isolation Forest</h2>
      {anomalyStats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <StatCard label="Total posts"     value={anomalyStats.total_posts}                          color="text-gray-800" />
          <StatCard label="Anomalies found" value={anomalyStats.anomaly_count}                        color="text-red-500" />
          <StatCard label="Normal posts"    value={anomalyStats.normal_count}                         color="text-green-600" />
          <StatCard label="Anomaly rate"    value={anomalyStats.anomaly_rate_percent + "%"}            color="text-amber-500" />
        </div>
      )}

      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Network Graph — networkx</h2>
      {graphStats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <StatCard label="Total nodes"   value={graphStats.total_nodes}    color="text-gray-800" />
          <StatCard label="Total edges"   value={graphStats.total_edges}    color="text-gray-800" />
          <StatCard label="Threat actors" value={graphStats.actor_nodes}    color="text-blue-600" />
          <StatCard label="Attack types"  value={graphStats.attack_type_nodes} color="text-red-500" />
        </div>
      )}

      <div className="bg-white rounded-xl border border-gray-200 p-4">
        <h2 className="text-sm font-semibold text-gray-600 mb-3">Pipeline summary</h2>
        <div className="space-y-2 text-sm text-gray-600">
          <div className="flex justify-between py-2 border-b border-gray-100">
            <span>NLP preprocessing</span>
            <span className="text-green-600 font-medium">spaCy + NLTK</span>
          </div>
          <div className="flex justify-between py-2 border-b border-gray-100">
            <span>Topic modeling</span>
            <span className="text-green-600 font-medium">LDA — 10 topics</span>
          </div>
          <div className="flex justify-between py-2 border-b border-gray-100">
            <span>Threat classification</span>
            <span className="text-green-600 font-medium">Random Forest — TF-IDF</span>
          </div>
          <div className="flex justify-between py-2 border-b border-gray-100">
            <span>Anomaly detection</span>
            <span className="text-green-600 font-medium">Isolation Forest — 5% contamination</span>
          </div>
          <div className="flex justify-between py-2">
            <span>Graph analysis</span>
            <span className="text-green-600 font-medium">networkx — co-occurrence</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ModelStats