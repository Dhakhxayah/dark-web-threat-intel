import useTopics from "../hooks/useTopics"
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts"

const COLORS = ["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd", "#818cf8", "#4f46e5", "#7c3aed", "#9333ea", "#a855f7", "#d946ef"]

function Topics() {
  const topics = useTopics()

  const chartData = topics.map((t) => ({
    name: t.label.length > 20 ? t.label.slice(0, 20) + "..." : t.label,
    posts: t.post_count,
    topic_id: t.topic_id,
  }))

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Topic Trends</h1>
      <p className="text-gray-500 text-sm mb-6">What threat themes are dominating forum chatter</p>

      {topics.length === 0 && (
        <p className="text-gray-400 text-sm">No topic data yet. Run the topic model first.</p>
      )}

      {topics.length > 0 && (
        <>
          <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6">
            <h2 className="text-sm font-semibold text-gray-600 mb-4">Posts per topic</h2>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={chartData} margin={{ left: 0, right: 10, top: 5, bottom: 60 }}>
                <XAxis dataKey="name" angle={-35} textAnchor="end" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="posts" radius={[4, 4, 0, 0]}>
                  {chartData.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {topics.map((topic) => (
              <div key={topic.topic_id} className="bg-white rounded-xl border border-gray-200 p-4">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="text-sm font-semibold text-gray-800">{topic.label}</h3>
                  <span className="text-xs text-gray-400">{topic.post_count} posts</span>
                </div>
                <div className="flex flex-wrap gap-1">
                  {topic.top_words.slice(0, 8).map((word) => (
                    <span key={word} className="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full">
                      {word}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

export default Topics