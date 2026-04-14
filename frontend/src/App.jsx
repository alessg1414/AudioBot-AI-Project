import { useState, useEffect, useRef } from 'react'
import './App.css'

const API_BASE = '/api'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [ready, setReady] = useState(null)
  const [toast, setToast] = useState(null)
  const messagesEndRef = useRef(null)

  const showToast = (message) => {
    setToast(message)
    setTimeout(() => setToast(null), 5000)
  }

  useEffect(() => {
    fetch(`${API_BASE}/status`)
      .then(res => res.json())
      .then(data => setReady(data.ready))
      .catch(() => setReady(false))
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    const question = input.trim()
    if (!question || loading) return

    setMessages(prev => [...prev, { role: 'user', text: question }])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch(`${API_BASE}/ask?q=${encodeURIComponent(question)}`)
      const data = await res.json()
      if (data.error === 'rate_limit') {
        showToast('Se ha alcanzado el límite diario de solicitudes a la API. Inténtelo de nuevo más tarde.')
      } else if (data.error === 'unavailable') {
        showToast('El modelo está experimentando una alta demanda. Inténtelo de nuevo en un momento.')
      } else if (data.error) {
        setMessages(prev => [...prev, { role: 'bot', text: `Error: ${data.error}` }])
      } else {
        setMessages(prev => [...prev, { role: 'bot', text: data.answer }])
      }
    } catch {
      setMessages(prev => [...prev, { role: 'bot', text: 'Error de conexión con el servidor.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-app">
      {toast && (
        <div className="toast">
          <span>{toast}</span>
          <button className="toast-close" onClick={() => setToast(null)}>✕</button>
        </div>
      )}
      <header className="chat-header">
        <h1>Audio Bot</h1>
        <span className={`status-dot ${ready ? 'online' : 'offline'}`} />
        <span className="status-text">
          {ready === null ? 'Conectando...' : ready ? 'Transcripción lista' : 'Sin transcripción'}
        </span>
      </header>

      <main className="chat-messages">
        {!ready && ready !== null && (
          <div className="system-message">
            No hay transcripción disponible. Asegúrese de precargar el audio a transcribir.
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="bubble">{msg.text}</div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="bubble typing">
              <span /><span /><span />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      <form className="chat-input" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder={ready ? 'Escribe tu pregunta sobre la llamada...' : 'Esperando transcripción...'}
          disabled={!ready || loading}
        />
        <button type="submit" disabled={!ready || loading || !input.trim()}>
          Enviar
        </button>
      </form>
    </div>
  )
}

export default App
