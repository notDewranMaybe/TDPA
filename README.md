<h1 align="center">🌾 农作物病虫害智能问答系统（RAG） / Crop Disease & Pest RAG System</h1>

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

</details>
中文版本
<details> <summary><b>点击展开 / Click to expand</b></summary>
🌿 项目简介
本项目旨在帮助农业科研人员和农技人员构建一个本地可运行的 RAG（Retrieval-Augmented Generation）系统，通过知识检索 + 大模型推理，实现农作物病虫害的智能问答与诊断建议。

主要功能：

数据 → 向量化 → FAISS 知识库

选择本地大语言模型（ChatGLM、Qwen、LLaMA）

双库融合检索（结构化知识 + 语义问答）

本地 Streamlit 网页交互
