
---

## 📄 `README.en.md`

```markdown
# 🌾 Crop Disease & Pest RAG System

[🇨🇳 中文](README.md) | [🇬🇧 English](README.en.md)

A **retrieval-augmented generation (RAG)** system for crop disease & pest diagnosis, powered by **local LLM**, **FAISS vector DB**, and **Streamlit web UI**.

---

## 📌 Overview

This project helps agricultural researchers and extension workers build a fully local crop disease Q&A system by combining:
- Structured knowledge + Semantic retrieval
- Local LLM reasoning
- Real-time web interaction

**Core features:**
- CSV data → vectorization → FAISS index
- Support for local LLM (ChatGLM / Qwen / LLaMA)
- Dual-base retrieval pipeline
- Streamlit front-end

---

## 🧩 Environment Setup

```bash
conda create -n cropRAG python=3.10
conda activate cropRAG
pip install -r requirements.txt
