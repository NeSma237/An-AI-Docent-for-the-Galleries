import json

with open(r"D:\ArtMuse\data\artworks.json", encoding="utf-8") as f:
    data = json.load(f)

target_id = 437792  # غيّريه لو الرقم المكرر يظهر مختلف عندك

matches = [art for art in data if art.get("id") == target_id]

print(f"عدد اللوحات اللي عندها id={target_id}: {len(matches)}\n")

for i, art in enumerate(matches, start=1):
    print(f"--- النسخة {i} ---")
    print("name:", art.get("name"))
    print("year:", art.get("year"))
    print("dimensions:", art.get("dimensions"))
    print("image_file:", art.get("image_file"))
    print()
