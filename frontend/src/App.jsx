import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom"
import AlertFeed from "./pages/AlertFeed"
import Topics from "./pages/Topics"
import AnomalyTimeline from "./pages/AnomalyTimeline"
import GraphExplorer from "./pages/GraphExplorer"

function Navbar() {
  const base = "px-4 py-2 rounded-lg text-sm font-medium transition-colors "
  const active = base + "bg-indigo-600 text-white"
  const inactive = base + "text-gray-600 hover:bg-gray-100"

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-3 flex items-center gap-2">
      <span className="text-sm font-bold text-gray-900 mr-4">ThreatIntel</span>
      <NavLink to="/" end className={({ isActive }) => isActive ? active : inactive}>Alerts</NavLink>
      <NavLink to="/topics" className={({ isActive }) => isActive ? active : inactive}>Topics</NavLink>
      <NavLink to="/anomalies" className={({ isActive }) => isActive ? active : inactive}>Anomalies</NavLink>
      <NavLink to="/graph" className={({ isActive }) => isActive ? active : inactive}>Network</NavLink>
    </nav>
  )
}

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<AlertFeed />} />
          <Route path="/topics" element={<Topics />} />
          <Route path="/anomalies" element={<AnomalyTimeline />} />
          <Route path="/graph" element={<GraphExplorer />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App