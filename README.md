# 🎧 AudioBot AI — Call Center Audio Analyzer

An AI-powered chatbot that transcribes call center audio recordings using OpenAI Whisper and lets you ask questions about the conversation through a RAG pipeline powered by Google Gemini and LlamaIndex.

## 📦 Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- [ffmpeg](https://ffmpeg.org/) (required by Whisper)
- A [Google Gemini API key](https://aistudio.google.com/apikey)
- NVIDIA GPU recommended (CUDA-enabled PyTorch for faster transcription)

### Backend

```bash
cd backend
pip install -r requirements.txt
```

**(Optional) For NVIDIA GPU acceleration:**

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu126 --force-reinstall
```

Create a `backend/.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
TRANSCRIPTION_PATH=C:\audio\call.txt
```

### Frontend

```bash
cd frontend
npm install
```

## 🛠 Usage

The project runs in three phases:

### 1. Transcribe Audio

Place your audio file at the path configured in `LoadAudio.py` (default: `C:\audio\Grabacion.mp3`) and run:

```bash
cd backend
python LoadAudio.py
```

This generates a `call.txt` file with the full transcription and timestamped segments.

### 2. Start the Backend Server

```bash
cd backend
python app.py
```

The Flask server starts at `http://localhost:8090`. It loads the transcription, builds a vector index, and exposes a query API.

### 3. Start the Frontend

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser and start asking questions about the call.

## ✨ Features

- **GPU-accelerated transcription** — Automatically uses CUDA if available (tested on RTX 4070 Super)
- **Whisper large-v3** — Maximum accuracy speech-to-text with beam search and optimized parameters
- **RAG-based Q&A** — Questions are answered strictly from the call content, not general knowledge
- **System prompt guard** — The bot refuses to answer questions unrelated to the call transcription
- **Timestamped segments** — The transcription output includes per-segment timestamps
- **Real-time chat UI** — Clean React interface with typing indicators and auto-scroll
> **Note:** The system is configured for Spanish. Whisper transcribes with `language="es"`, the system prompt and UI labels are in Spanish, and error messages displayed to the user are also in Spanish.

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Transcription | OpenAI Whisper (large-v3) + PyTorch CUDA |
| LLM | Google Gemini 2.5 Flash |
| Embeddings | Gemini Embedding 001 |
| RAG Framework | LlamaIndex (VectorStoreIndex) |
| Backend | Flask + flask-cors |
| Frontend | React 19 + Vite |

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/status` | Returns `{"ready": true/false}` depending on whether a transcription is loaded |
| `GET` | `/ask?q=<question>` | Queries the RAG engine and returns `{"answer": "..."}` |

## 📄 License

MIT License

## 🙌 Credits

- [OpenAI Whisper](https://github.com/openai/whisper) for speech-to-text
- [LlamaIndex](https://github.com/run-llama/llama_index) for the RAG pipeline
- [Google Gemini](https://ai.google.dev/) for LLM and embeddings
