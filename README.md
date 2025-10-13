# 🌾 虫儿食农油，百秒则灰白
——从0到1的「查出病」双库RAG智能体搭建教程

> 本项目旨在提供一个入门级RAG智能体无痛出生的保姆级教程。
> 0显卡、0服务器，也能开箱即用上手部署！  

---

## 📌 项目简介

你是不是也遇到过这样的情况：
- 📂 手头有一堆小数据但不知道该怎么处理？  
- 🧠 想搭一个 Agent，但服务器 / GPU / 算力统统没有？  
- 🐣 新人入门，大佬教程太抽象，不知从何下手？

「查出病」Is ALL you need!

「查出病」是一个能在**短时间内迅速复现**，支持**自定义数据处理**的双数据库农业病虫害检索增强生成(RAG)智能体。

它可以：

- **处理病虫害知识 → 向量化 → FAISS 双库存储**
- **选你喜欢的本地 LLM（ChatGLM / Qwen / LLaMA）自由回答**  
- **双库融合检索 → 智能生成问答**  
- **Streamlit 网页互动 → 主动给作物查查病** 
---

## 📁 「查出病」结构

```python

TDPA/
|
├── data/               # 原始 & 处理后数据 CSV/JSON
├── embeddings/         # FAISS 向量库索引文件
├── models/             # 本地 LLM 模型
├── scripts/            # 数据处理 & RAG 脚本
├── app.py              # Streamlit 前端入口
├── requirements.txt    # Python 依赖列表
└── README.md           # 教程说明
```

## 🛠️ 系统搭建思路

### 1️⃣ 环境准备

💻 推荐电脑配置与参数
```
类型	    最低配置	                  推荐配置	                
CPU	      i5 / Ryzen 5	            i7 / Ryzen 7	        
内存	     ≥ 8GB	                   16GB+	            
GPU	      无（CPU 模式）           NVIDIA 3060 / 4060 8GB+	
显存	      无	                   ≥ 8GB	
硬盘	     50GB	                 SSD 100GB+	
系统	  Win10 / Ubuntu 20.04	Ubuntu 22.04 LTS,Linux 更稳定
Python	     3.8+	                 3.10（推荐）	
```

使用 Conda 创建独立环境并安装依赖：

```bash
conda create -n ccb python=3.10
conda activate ccb
pip install -需要模块，

根据模型需求安装版本，推荐先去huggingface链接下确定，不然容易导致“依赖地狱”被迫重下环境。
```
### 2️⃣ 本地大语言模型选择与加载
```
模型	        显存需求	      语言支持	        特点
ChatGLM3-6B	    ≥ 8GB	        中文	    响应快，中文理解强
Qwen-1.8B / 4B	≥ 4GB / 6GB	    中英	    小巧灵活，易部署
LLaMA2-7B	    ≥ 12GB	        多语种	    英文强，需高显存
Phi-3-mini	    ≥ 2GB	        中英	    轻量，CPU 友好
```

加载示例：
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "zai-org/chatglm3-6b"#或者你的本地路径，填写zai-org则默认从huggingface开始下载，容易被墙，建议提前下载到本地
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
```

✨ 无 GPU 或 GPU 太小可采用量化加载（4bit / 8bit）或 CPU 推理模式，量化方法以及提示词模板相关详见这篇CSDN，推荐入门快速扫盲：https://blog.csdn.net/weixin_42426841/article/details/142834780

### 3️⃣ 数据向量化与知识库构建

如果需要自定义数据，请提前制定标准进行清洗，此处以仓库内的json列表类型文件为例，展示数据的向量化与嵌入的流程，完整代码在Data_Vectorization_FAISS获取。

```python
import json
import torch
from transformers import AutoTokenizer, AutoModel
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

json_file = "final_disease_data.json"             # 仓库中已给出JSON文件，如果需要自定义数据需要提前清洗
model_path = "你的本地路径/text2vec-base-chinese"       # 本地模型路径
faiss_index_path = "disease_faiss_index"         # 向量库保存路径
```

本项目是受CropDP-KG文章启发制作而成，原文链接：https://www.nature.com/articles/s41597-025-04492-0，

中文数据访问：https://github.com/dadadaray/CropDP-KG/tree/Knowledge-System。

英文QA问答数据访问：https://github.com/UnicomAI/UnicomBenchmark/tree/main/CDDMBench。

想从基本的NLP基础开始学习/补充知识可参考华东师范大学著名的Agricultural Knowledge Graph仓库: https://github.com/qq547276542/Agriculture_KnowledgeGraph，

以及东南大学汪鹏老师的研究生课程《知识图谱》：https://github.com/npubird/KnowledgeGraphCourse

深入学习可参考吴恩达先生的Sequence Models,Agentic AI等系列课程，课程链接：https://www.deeplearning.ai/courses/agentic-ai/?utm_campaign=agentic-ai-launch&utm_medium=hero-takeover&utm_source=dlai-homepage

### 4️⃣ RAG 流程与前端交互（Streamlit）

**RAG核心逻辑：**

*用户输入问题 → 向 FAISS 检索相似内容 → 拼接上下文作为提示 → 传入 LLM 生成回答*

本文搭建的RAG是一个双库RAG，中文库直接检索，英文库严格翻译后检索，拼接结果再翻译成中文结合权重，默认中文数据权重0.7，英文qa权重0.3，进行双库检索输出。

如果只需要单库模式，需要将代码中ask_question_dual，load_faiss_dual函数与Streamlit交互界面进行修改，或者上传.py文件给其他LLM协助修改。

使用到的完整代码可在Dual_RAG.py获取，

关于RAG的快速入门可参考这篇CSDN：https://blog.csdn.net/a2875254060/article/details/142468037

**Streamlit运行命令：**

```streamlit run app.py```

它可以：

🧩 输入问题 → 自动检索知识库

💬 思考回答 + 参考来源展示，信息全程透明化

⏳ 历史文本保存 + Fallback机制通识回答

🚀 快速关键词检索作物病害，飞速查病

### ⭐本文仅提供一个最基本的双库文本RAG框架和数据，欢迎开箱抱走客制化，让「查出病」不断进化！
