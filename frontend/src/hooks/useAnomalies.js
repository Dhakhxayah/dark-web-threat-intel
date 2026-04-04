import { useEffect } from "react"
import { fetchAnomalyTimeline, fetchAnomalyStats } from "../api/anomalies"
import useStore from "../store/useStore"

function useAnomalies() {
  const setAnomalies = useStore((s) => s.setAnomalies)
  const setAnomalyStats = useStore((s) => s.setAnomalyStats)
  const anomalies = useStore((s) => s.anomalies)
  const anomalyStats = useStore((s) => s.anomalyStats)

  useEffect(() => {
    fetchAnomalyTimeline()
      .then((res) => setAnomalies(res.data.timeline || []))
      .catch((err) => console.error("Anomaly timeline error:", err))
    fetchAnomalyStats()
      .then((res) => setAnomalyStats(res.data))
      .catch((err) => console.error("Anomaly stats error:", err))
  }, [])

  return { anomalies, anomalyStats }
}

export default useAnomalies
