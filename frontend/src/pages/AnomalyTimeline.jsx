import useAnomalies from "../hooks/useAnomalies"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts"

function StatCard({ label, value, color }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4 flex flex-col gap-1">
      <span className="text-xs text-gray-400">{label}</span>
      <span className={"text-2xl font-bold " + color}>{value}</span>
    </div>
  )
}

function AnomalyTimeline() {
  const { anomalies, anomalyStats } = useAnomalies()

  const chartData = anomalies.map((d) => ({
    date: d.date,
    total: d.total_posts,
    anomalies: d.anomaly_count,
  }))

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Anomaly Timeline</h1>
      <p className="text-gray-500 text-sm mb-6">When did unusual spikes and patterns occur</p>

      {anomalyStats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <StatCard label="Total posts" value={anomalyStats.total_posts} color="text-gray-800" />
          <StatCard label="Anomalies found" value={anomalyStats.anomaly_count} color="text-purple-600" />
          <StatCard label="Normal posts" value={anomalyStats.normal_count} color="text-green-600" />
          <StatCard label="Anomaly rate" value={anomalyStats.anomaly_rate_percent + "%"} color="text-red-500" />
        </div>
      )}

      {chartData.length === 0 && (
        <p className="text-gray-400 text-sm">No timeline data yet. Run anomaly detection first.</p>
      )}

      {chartData.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <h2 className="text-sm font-semibold text-gray-600 mb-4">Posts vs anomalies over time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData} margin={{ left: 0, right: 10, top: 5, bottom: 5 }}>
              <XAxis dataKey="date" tick={{ fontSize: 10 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="total" stroke="#6366f1" strokeWidth={2} dot={false} name="Total posts" />
              <Line type="monotone" dataKey="anomalies" stroke="#ef4444" strokeWidth={2} dot={false} name="Anomalies" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

export default AnomalyTimeline