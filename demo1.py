import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# 设置本地模型路径
model_path = "/root/autodl-tmp/TDPA/LLM"

# 手动加载本地模型和分词器
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True)

# 测试模型是否能正常推理
input_text = "你好，ChatGLM3-6B！"
inputs = tokenizer(input_text, return_tensors="pt")

# 在 GPU 上推理
inputs = {k: v.to(model.device) for k, v in inputs.items()}
outputs = model.generate(inputs["input_ids"], max_length=50)

# 解码生成的文本
output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(output_text)
