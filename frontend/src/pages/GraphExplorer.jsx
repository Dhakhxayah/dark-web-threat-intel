import { useState } from "react"
import useGraph from "../hooks/useGraph"
import { fetchNodeConnections } from "../api/graph"

const NODE_COLORS = {
  actor: "bg-blue-100 text-blue-800",
  keyword: "bg-green-100 text-green-800",
  attack_type: "bg-red-100 text-red-800",
}

function GraphExplorer() {
  const { graph, graphStats } = useGraph()
  const [selectedNode, setSelectedNode] = useState(null)
  const [connections, setConnections] = useState(null)
  const [search, setSearch] = useState("")

  function handleNodeClick(node) {
    setSelectedNode(node)
    fetchNodeConnections(node.id)
      .then((res) => setConnections(res.data))
      .catch((err) => console.error("Connection error:", err))
  }

  const filteredNodes = graph
    ? graph.nodes.filter((n) =>
        n.label.toLowerCase().includes(search.toLowerCase())
      ).slice(0, 80)
    : []

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Network Explorer</h1>
      <p className="text-gray-500 text-sm mb-6">Click any node to see its threat connections</p>

      {graphStats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-xl border border-gray-200 p-3">
            <p className="text-xs text-gray-400">Total nodes</p>
            <p className="text-xl font-bold text-gray-800">{graphStats.total_nodes}</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-3">
            <p className="text-xs text-gray-400">Total edges</p>
            <p className="text-xl font-bold text-gray-800">{graphStats.total_edges}</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-3">
            <p className="text-xs text-gray-400">Threat actors</p>
            <p className="text-xl font-bold text-blue-600">{graphStats.actor_nodes}</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-3">
            <p className="text-xs text-gray-400">Attack types</p>
            <p className="text-xl font-bold text-red-500">{graphStats.attack_type_nodes}</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <input
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm mb-4"
            placeholder="Search nodes..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <div className="overflow-y-auto max-h-96 space-y-2">
            {filteredNodes.length === 0 && (
              <p className="text-gray-400 text-sm">No graph data yet. Run graph builder first.</p>
            )}
            {filteredNodes.map((node) => (
              <div
                key={node.id}
                onClick={() => handleNodeClick(node)}
                className={"flex justify-between items-center p-2 rounded-lg cursor-pointer hover:bg-gray-50 border " +
                  (selectedNode && selectedNode.id === node.id ? "border-indigo-300 bg-indigo-50" : "border-transparent")}
              >
                <div className="flex items-center gap-2">
                  <span className={"text-xs px-2 py-0.5 rounded-full font-medium " + (NODE_COLORS[node.node_type] || "bg-gray-100 text-gray-600")}>
                    {node.node_type}
                  </span>
                  <span className="text-sm text-gray-700">{node.label}</span>
                </div>
                <span className="text-xs text-gray-400">{node.degree} links</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl border border-gray-200 p-4">
          {!selectedNode && (
            <p className="text-gray-400 text-sm mt-8 text-center">Select a node to see its connections</p>
          )}
          {selectedNode && (
            <>
              <h2 className="text-sm font-semibold text-gray-800 mb-1">{selectedNode.label}</h2>
              <p className="text-xs text-gray-400 mb-4">{selectedNode.degree} connections</p>
              {connections && (
                <div className="space-y-2 overflow-y-auto max-h-80">
                  {connections.connected_nodes.map((node) => (
                    <div
                      key={node.id}
                      className="flex justify-between items-center p-2 rounded-lg bg-gray-50"
                    >
                      <div className="flex items-center gap-2">
                        <span className={"text-xs px-2 py-0.5 rounded-full " + (NODE_COLORS[node.node_type] || "bg-gray-100 text-gray-600")}>
                          {node.node_type}
                        </span>
                        <span className="text-sm text-gray-700">{node.label}</span>
                      </div>
                      <span className="text-xs text-gray-400">{node.degree} links</span>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default GraphExplorer