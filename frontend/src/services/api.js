import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' }
})

export const predictLoan = (application) =>
  api.post('/predict', application).then(r => r.data)

export const explainDecision = (application) =>
  api.post('/explain', application).then(r => r.data)

export const getBiasReport = () =>
  api.get('/bias-report').then(r => r.data)

export const submitAppeal = (payload) =>
  api.post('/appeal', payload).then(r => r.data)

export const sendChatMessage = (payload) =>
  api.post('/chat', payload).then(r => r.data)
