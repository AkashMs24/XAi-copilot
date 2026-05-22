import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Predict from './pages/Predict'
import BiasReport from './pages/BiasReport'
import Appeal from './pages/Appeal'
import Copilot from './pages/Copilot'
import Whatif from './pages/whatif'
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index         element={<Dashboard />} />
        <Route path="predict" element={<Predict />} />
        <Route path="whatif"  element={<Whatif />} />
        <Route path="bias"    element={<BiasReport />} />
        <Route path="appeal"  element={<Appeal />} />
        <Route path="copilot" element={<Copilot />} />
      </Route>
    </Routes>
  )
}
