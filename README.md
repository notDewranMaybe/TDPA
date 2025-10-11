# 🌾 农作物病虫害智能问答系统（RAG）

[🇨🇳 中文](README.md) | [🇬🇧 English](README.en.md)

基于本地大语言模型（LLM）、FAISS 向量数据库与 Streamlit 前端的**农作物病虫害智能问答与诊断系统**。

---

## 📌 项目简介

本项目旨在帮助农业科研人员和农技人员构建一个本地可运行的 RAG（Retrieval-Augmented Generation）系统，通过知识检索+大模型推理，实现农作物病虫害的智能问答和诊断建议。

**主要功能：**
- 数据 → 向量化 → FAISS 知识库
- 选择本地大语言模型（如 ChatGLM、Qwen、LLaMA）
- 双库融合检索（结构化知识 + 语义问答）
- 本地 Streamlit 网页交互

---

## 🧩 环境配置

```bash
conda create -n cropRAG python=3.10
conda activate cropRAG
pip install -r requirements.txt
