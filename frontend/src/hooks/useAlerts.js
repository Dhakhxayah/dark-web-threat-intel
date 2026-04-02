import { useEffect } from "react"
import { fetchAlerts } from "../api/alerts"
import useStore from "../store/useStore"

function useAlerts(limit, minRisk, threatType) {
  const setAlerts = useStore((s) => s.setAlerts)
  const setLoading = useStore((s) => s.setLoading)
  const setError = useStore((s) => s.setError)
  const alerts = useStore((s) => s.alerts)

  useEffect(() => {
    setLoading(true)
    fetchAlerts(limit, minRisk, threatType)
      .then((res) => {
        setAlerts(res.data.alerts || [])
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [limit, minRisk, threatType])

  return alerts
}

export default useAlerts