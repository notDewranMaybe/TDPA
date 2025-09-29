# -*- coding: utf-8 -*-
import json
import torch
from transformers import AutoTokenizer, AutoModel
from langchain_community.vectorstores import FAISS

# ==== 配置路径 ====
json_file = "final_disease_data.json"             # 已生成的 JSON
model_path = "/root/text2vec-base-chinese"       # 本地模型路径
faiss_index_path = "disease_faiss_index"         # 向量库保存路径

# ==== 1. 加载本地模型 ====
print("加载本地模型...")
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModel.from_pretrained(model_path, local_files_only=True)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

# ==== 2. 读取 JSON 数据 ====
print("读取 JSON 数据...")
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, dict):
    data_list = list(data.values())
else:
    data_list = data

# ==== 3. 生成文本和 metadata ====
print("生成文本和 metadata...")
texts = []
metadatas = []
for d in data_list:
    text_parts = [
        d.get("name") or "",
        d.get("english") or "",
        " ".join(d.get("symptom", [])),
        " ".join(d.get("crop", [])),
        " ".join(d.get("part", [])),
        " ".join(d.get("area", [])),
        " ".join(d.get("condition", [])),
        " ".join(d.get("temperature", [])),
        d.get("intro") or "",
        d.get("harm") or "",
        d.get("rule") or ""
    ]
    text = " ".join([t for t in text_parts if t])
    texts.append(text)
    # metadata 中同时保留文本
    metadatas.append({"name": d.get("name"), "english": d.get("english"), "text": text})

# ==== 4. 生成 embeddings（mean pooling + batch） ====
print("生成 embeddings...")
batch_size = 16
all_embeddings = []
with torch.no_grad():
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        enc = tokenizer(batch_texts, padding=True, truncation=True, max_length=512, return_tensors="pt")
        enc = {k: v.to(device) for k, v in enc.items()}
        outputs = model(**enc)
        # mean pooling, 忽略 padding
        attention_mask = enc["attention_mask"].unsqueeze(-1)
        sum_embeddings = (outputs.last_hidden_state * attention_mask).sum(dim=1)
        lengths = attention_mask.sum(dim=1)
        embeddings = sum_embeddings / lengths
        all_embeddings.append(embeddings.cpu())

# 转成 list
embeddings_tensor = torch.cat(all_embeddings, dim=0)

# ==== 5. 建立 FAISS 向量库（用 from_texts 代替 from_embeddings） ====
print("建立 FAISS 向量库...")
# 注意：from_texts 会自己生成 embeddings，需要我们传入 embeddings 实例
from langchain.embeddings import HuggingFaceEmbeddings

# 构造 embeddings 接口
class LocalEmbeddingWrapper:
    def __init__(self, embeddings_tensor):
        self.embeddings = embeddings_tensor

    def embed_documents(self, texts):
        # 返回对应 embeddings
        return self.embeddings.tolist()

    def embed_query(self, text):
        raise NotImplementedError

# 使用包装类
embedding_wrapper = LocalEmbeddingWrapper(embeddings_tensor)

vector_store = FAISS.from_texts(texts, embedding_wrapper, metadatas=metadatas)


# ==== 6. 保存 FAISS 向量库 ====
print(f"保存 FAISS 向量库到 {faiss_index_path} ...")
vector_store.save_local(faiss_index_path)


print("完成！本地向量库已生成，可用于检索或问答。")
