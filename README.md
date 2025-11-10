# Building-e2e-google-adk-agent-applications---using-codelabs

# Agentic Multimodal E2E App (ADK + Agentic RAG)

Full-stack agent that accepts **text + images**, uses **Agentic RAG** over a DB + vector store, and serves a **web UI**. Deployed on Cloud Run.

---

## 📌 Submission Links
- **Live Demo URL:** https://<your-cloud-run-service>.run.app
- **GitHub Repo:** https://github.com/<you>/<repo>
- **Walkthrough Video (5–10 min):** https://youtu.be/<id>

> The video shows: architecture → code tour → ingest image → ask questions → citations → (optional) deployment.

---

## ✨ Features (Rubric Mapping)
- **End-to-End**: UI → API → DB/Vector → grounded answers
- **Multimodal**: image/PDF ingestion (e.g., receipts) + text
- **Agentic RAG**: tool-calling to store, retrieve, and analyze
- **Database Integration**: Firestore (Native) + vector search
- **Artifacts**: GCS bucket for uploaded files
- **Deployment**: Cloud Run + `/healthz` liveness

---

## 🧰 Tech Stack
Python 3.12 · FastAPI · Google **Agent Development Kit (ADK)** · **Gemini 2.5** · Firestore (vectors) · GCS · Gradio UI · Docker · Cloud Run

---

## 📂 Repo Layout
