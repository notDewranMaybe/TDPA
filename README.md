<h1 align="center">🌾 Talk to Da Plant, it Answers!--- A 0 to 1 dual database RAG tutorial</h1>

<p align="center">
  <b>Language / 语言：</b>
  <a href="#english-version">English</a> | <a href="#中文版本">中文</a>
</p>

---

## English Version
<details open>
<summary><b>Click to collapse / 点击折叠</b></summary>

### 🌿 Overview

This project is a **local Retrieval-Augmented Generation (RAG)** system designed to assist agricultural researchers and technicians in diagnosing crop diseases and pests through intelligent Q&A.

**Main Features:**
- Data → Vectorization → FAISS Knowledge Base  
- Supports local LLMs (ChatGLM / Qwen / LLaMA)  
- Dual-retrieval (structured knowledge + semantic reasoning)  
- Interactive local Streamlit web interface  

---

### 🧩 Environment Setup

```bash
conda create -n cropRAG python=3.10
conda activate cropRAG
pip install -r requirements.txt
