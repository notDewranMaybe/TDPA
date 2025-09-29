import pandas as pd

csv_files = {
    "sym": "autodl-tmp/TDPA/data/relationsym.csv",
    "crop": "autodl-tmp/TDPA/data/relationcrop.csv",
    "part": "autodl-tmp/TDPA/data/relationpart.csv",
    "area": "autodl-tmp/TDPA/data/relationarea.csv",
    "con": "autodl-tmp/TDPA/data/relationcon.csv",
    "tem": "autodl-tmp/TDPA/data/relationtem.csv",
    "eng": "autodl-tmp/TDPA/data/relationEng.csv",
}

for key, path in csv_files.items():
    try:
        df = pd.read_csv(path, nrows=3)  # 只读3行就够
        print(f"\n=== {key} ({path}) ===")
        print("列名:", list(df.columns))
        print(df.head(3))
    except Exception as e:
        print(f"读取 {path} 出错: {e}")
