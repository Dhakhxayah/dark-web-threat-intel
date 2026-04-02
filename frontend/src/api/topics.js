import client from "./client"

export function fetchTopics() {
  return client.get("/api/v1/topics/")
}

export function fetchTrendingTopics() {
  return client.get("/api/v1/topics/trending")
}

export function fetchTopicPosts(topicId, limit = 20) {
  return client.get("/api/v1/topics/" + topicId, { params: { limit } })
}