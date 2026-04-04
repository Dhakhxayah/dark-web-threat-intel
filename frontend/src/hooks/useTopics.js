import { useEffect } from "react"
import { fetchTrendingTopics } from "../api/topics"
import useStore from "../store/useStore"

function useTopics() {
  const setTopics = useStore((s) => s.setTopics)
  const topics = useStore((s) => s.topics)

  useEffect(() => {
    fetchTrendingTopics()
      .then((res) => setTopics(res.data.trending || []))
      .catch((err) => console.error("Topics error:", err))
  }, [])

  return topics
}

export default useTopics
