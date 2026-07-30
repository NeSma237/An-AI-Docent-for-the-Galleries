import json
import os

JSON_PATH = r"D:\ArtMuse\data\artworks.json"
BACKUP_PATH = r"D:\ArtMuse\data\artworks_backup.json"

# ==========================================
# تحميل الملف
# ==========================================

with open(JSON_PATH, "r", encoding="utf-8") as f:
    artworks = json.load(f)

print(f"عدد اللوحات قبل التنظيف: {len(artworks)}")

# ==========================================
# نسخة احتياطية أولًا (أهم خطوة قبل أي حذف)
# ==========================================

with open(BACKUP_PATH, "w", encoding="utf-8") as f:
    json.dump(artworks, f, ensure_ascii=False, indent=4)

print(f"تم حفظ نسخة احتياطية في: {BACKUP_PATH}")

# ==========================================
# حذف التكرار: بيسيب أول ظهور للـ id ويشيل أي تكرار بعده
# ==========================================

seen_ids = set()
cleaned = []
removed = []

for art in artworks:
    aid = art.get("id")
    if aid in seen_ids:
        removed.append(art.get("name"))
        continue
    seen_ids.add(aid)
    cleaned.append(art)

print(f"\nعدد اللوحات بعد التنظيف: {len(cleaned)}")

if removed:
    print("\nاللوحات اللي اتشالت (نسخ مكررة):")
    for name in removed:
        print(f"  - {name}")
else:
    print("\nمفيش تكرار اتشال، الملف كان نضيف أصلاً.")

# ==========================================
# حفظ النسخة النضيفة
# ==========================================

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=4)

print(f"\n✅ تم حفظ الملف النضيف في: {JSON_PATH}")
print(f"   (النسخة القديمة محفوظة كنسخة احتياطية في artworks_backup.json)")