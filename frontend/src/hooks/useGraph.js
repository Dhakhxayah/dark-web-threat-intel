import { useEffect } from "react"
import { fetchFullGraph, fetchGraphStats } from "../api/graph"
import useStore from "../store/useStore"

function useGraph() {
  const setGraph = useStore((s) => s.setGraph)
  const setGraphStats = useStore((s) => s.setGraphStats)
  const graph = useStore((s) => s.graph)
  const graphStats = useStore((s) => s.graphStats)

  useEffect(() => {
    fetchFullGraph()
      .then((res) => setGraph(res.data.graph))
      .catch((err) => console.error("Graph error:", err))
    fetchGraphStats()
      .then((res) => setGraphStats(res.data))
      .catch((err) => console.error("Graph stats error:", err))
  }, [])

  return { graph, graphStats }
}

export default useGraph
