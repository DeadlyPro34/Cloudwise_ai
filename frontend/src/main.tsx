import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

if (!import.meta.env.VITE_API_URL) {
  throw new Error("Missing VITE_API_URL in .env. Please set this environment variable.");
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
