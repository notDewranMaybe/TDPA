<h1 align="center">🌾 Crop Disease & Pest RAG System / 农作物病虫害智能问答系统</h1>

<p align="center">
  <b>Language / 语言：</b>
  <a href="#english-version">English</a> | <a href="#中文版本">中文</a>
</p>

---

## English Version

<details open>
<summary><b>Click to collapse / 点击折叠</b></summary>

### 🌿 Overview
A local Retrieval-Augmented Generation (RAG) system for crop disease & pest diagnosis, powered by **FAISS**, **local LLM**, and **Streamlit**.

**Features:**
- CSV → Vectorization → FAISS index  
- Local model loading (ChatGLM / Qwen / LLaMA)  
- Dual knowledge base retrieval  
- Streamlit Web UI  

### ⚙️ Setup
```bash
conda create -n cropRAG python=3.10
conda activate cropRAG
pip install -r requirements.txt
