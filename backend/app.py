import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

SYSTEM_PROMPT = PromptTemplate(
    "Eres un asistente especializado en analizar llamadas telefónicas de un Call Center. "
    "Solo puedes responder preguntas relacionadas con el contenido de la transcripción de la llamada proporcionada. "
    "Si el usuario pregunta algo que no tiene relación con la llamada, responde: "
    "'Lo siento, solo puedo responder preguntas relacionadas con el contenido de la llamada telefónica.'\n\n"
    "Contexto de la llamada:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Pregunta: {query_str}\n"
    "Respuesta: "
)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TRANSCRIPTION_PATH = os.getenv("TRANSCRIPTION_PATH", r"C:\audio\call.txt")

app = Flask(__name__)
CORS(app)

query_engine = None


def build_index():
    """Load call.txt and build a VectorStoreIndex with Gemini."""
    global query_engine

    if not os.path.exists(TRANSCRIPTION_PATH):
        print(f"Transcription file not found: {TRANSCRIPTION_PATH}")
        return False

    Settings.llm = GoogleGenAI(
        model="gemini-2.5-flash",
        api_key=GEMINI_API_KEY,
    )
    Settings.embed_model = GoogleGenAIEmbedding(
        model_name="gemini-embedding-001",
        api_key=GEMINI_API_KEY,
    )

    with open(TRANSCRIPTION_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    documents = [Document(text=text)]
    index = VectorStoreIndex.from_documents(
        documents,
        transformations=[SentenceSplitter(chunk_size=4096, chunk_overlap=200)],
    )
    query_engine = index.as_query_engine(
        text_qa_template=SYSTEM_PROMPT,
        similarity_top_k=3,
    )
    print("Index built successfully.")
    return True


@app.route("/status")
def status():
    ready = os.path.exists(TRANSCRIPTION_PATH) and query_engine is not None
    return jsonify({"ready": ready})


@app.route("/ask")
def ask():
    if query_engine is None:
        return jsonify({"error": "No transcription loaded. Run LoadAudio.py first."}), 503

    question = request.args.get("q", "").strip()
    if not question:
        return jsonify({"error": "Missing query parameter 'q'."}), 400

    try:
        response = query_engine.query(question)
        return jsonify({"answer": str(response)})
    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            return jsonify({"error": "rate_limit"}), 429
        if "503" in error_str or "UNAVAILABLE" in error_str:
            return jsonify({"error": "unavailable"}), 503
        return jsonify({"error": error_str}), 500


if __name__ == "__main__":
    print("Loading transcription and building index...")
    build_index()
    print(f"Server starting on http://localhost:8090")
    app.run(host="0.0.0.0", port=8090, debug=False)
