import { create } from "zustand"

const useStore = create((set) => ({
  alerts: [],
  topics: [],
  anomalies: [],
  graph: null,
  anomalyStats: null,
  graphStats: null,
  loading: false,
  error: null,

  setAlerts: (alerts) => set({ alerts }),
  setTopics: (topics) => set({ topics }),
  setAnomalies: (anomalies) => set({ anomalies }),
  setGraph: (graph) => set({ graph }),
  setAnomalyStats: (anomalyStats) => set({ anomalyStats }),
  setGraphStats: (graphStats) => set({ graphStats }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}))

export default useStore