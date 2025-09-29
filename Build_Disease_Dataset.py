import pandas as pd
import json
from collections import defaultdict

# ==== 配置路径 ====
csv_files = {
    "sym": "autodl-tmp/TDPA/data/relationsym.csv",
    "crop": "autodl-tmp/TDPA/data/relationcrop.csv",
    "part": "autodl-tmp/TDPA/data/relationpart.csv",
    "area": "autodl-tmp/TDPA/data/relationarea.csv",
    "con": "autodl-tmp/TDPA/data/relationcon.csv",
    "tem": "autodl-tmp/TDPA/data/relationtem.csv",
    "eng": "autodl-tmp/TDPA/data/relationEng.csv",
}
xls_file = "autodl-tmp/TDPA/data/disease_info.xls"
output_file = "autodl-tmp/TDPA/data/final_disease_data.json"

# ==== 初始化数据结构 ====
data = defaultdict(lambda: {
    "name": None,
    "english": None,
    "symptom": [],
    "crop": [],
    "part": [],
    "area": [],
    "condition": [],
    "temperature": [],
    "intro": "",
    "harm": "",
    "rule": ""
})

# ==== 辅助函数 ====
def normalize_entity(name):
    if not isinstance(name, str):
        return ""
    return name.strip().replace("\u3000", "")

# ==== CSV → JSON 字段映射 ====
csv_field_map = {
    "sym": ("symptom", "sym"),
    "crop": ("crop", "crop"),
    "part": ("part", "part"),
    "area": ("area", "area"),
    "con": ("condition", "condition"),
    "tem": ("temperature", "tem"),
    "eng": ("english", "english")
}

# ==== 读取 CSV ====
for key, path in csv_files.items():
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"读取 {path} 出错: {e}")
        continue

    field_name, col_name = csv_field_map[key]

    for _, row in df.iterrows():
        entity = normalize_entity(row.get("entity", ""))
        if not entity:
            continue

        if entity not in data:
            data[entity]["name"] = entity

        value = str(row.get(col_name, "")).strip()
        if not value:
            continue

        if field_name == "english":
            data[entity]["english"] = value
        else:
            data[entity][field_name].append(value)

# ==== 读取 Excel ====
try:
    xls_df = pd.read_excel(xls_file)
    for _, row in xls_df.iterrows():
        entity = normalize_entity(row.get("名称", ""))
        if not entity:
            continue

        if entity not in data:
            data[entity]["name"] = entity

        d = data[entity]
        for k, col in [("english", "英文名"),
                       ("intro", "简介"),
                       ("harm", "为害症状"),
                       ("rule", "发生规律")]:
            value = str(row.get(col, "") or "").strip()
            if value:
                d[k] = value
except Exception as e:
    print(f"读取 {xls_file} 出错: {e}")

# ==== 去重 ====
final_data = []
for entity, info in data.items():
    for key in ["symptom", "crop", "part", "area", "condition", "temperature"]:
        info[key] = list(set([x.strip() for x in info[key] if x and str(x).strip()]))
    final_data.append(info)

# ==== 输出 JSON ====
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"合并数据已输出到 {output_file}")
