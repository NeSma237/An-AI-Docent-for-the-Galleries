import json
import os
from collections import Counter

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ==========================================
# Paths
# ==========================================

# مسار نسبي بدل ما يكون مربوط بجهاز واحد بس (D:\ArtMuse\data)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

JSON_PATH = os.path.join(DATA_DIR, "artworks.json")

VECTOR_DB_PATH = os.path.join(DATA_DIR, "vector_db")

# ==========================================
# Load JSON
# ==========================================

with open(JSON_PATH, "r", encoding="utf-8") as f:
    artworks = json.load(f)

# ==========================================
# فحص وجود IDs مكررة قبل البناء
# (لو فيه تكرار، آخر لوحة بنفس الـ id هتلغي اللي قبلها في الاسترجاع)
# ==========================================

id_counts = Counter(art.get("id") for art in artworks)
duplicate_ids = [aid for aid, count in id_counts.items() if count > 1]

if duplicate_ids:
    print("⚠️  تحذير: فيه IDs مكررة في artworks.json:")
    for aid in duplicate_ids:
        names = [a.get("name") for a in artworks if a.get("id") == aid]
        print(f"   - id={aid} مستخدم في: {names}")
    print("   لازم تتصلح قبل ما تكمل، وإلا هتفقد لوحات من قاعدة البيانات.\n")

# ==========================================
# Convert JSON -> Documents
# ==========================================

documents = []

for art in artworks:

    interesting = art.get("interesting_facts", [])

    if isinstance(interesting, list):
        interesting = "\n".join(
            f"- {fact}" for fact in interesting
        )

    text = f"""
Artwork Name:
{art.get("name","")}

Artist:
{art.get("artist","")}

Year:
{art.get("year","")}

Style:
{art.get("style","")}

Department:
{art.get("department","")}

Materials:
{art.get("materials","")}

Story:
{art.get("story","")}

Symbols:
{art.get("symbols","")}

Artist Biography:
{art.get("artist_bio","")}

Historical Context:
{art.get("historical_context","")}

Interesting Facts:
{interesting}
"""

    doc = Document(
        page_content=text,
        metadata={
            "id": art.get("id"),
            "name": art.get("name"),
            "artist": art.get("artist"),
            "image_file": art.get("image_file"),
            "object_url": art.get("object_url")
        }
    )

    documents.append(doc)

print(f"Documents created: {len(documents)}")

# ==========================================
# ملحوظة: تم إلغاء خطوة الـ Splitting عن قصد.
#
# كل لوحة بتتحول لـ Document واحد كامل (مش بيتقسم لأجزاء/chunks).
# السبب: لو قسّمنا كل لوحة لعدة chunks، فـ retrieval.py بيسحب
# أعلى قطعة واحدة بس (k=1) ممكن ترجع بدون الـ Symbols أو الـ Story
# لو وقعوا في chunk تاني منفصل عن اللي اترجع. بما إن حجم كل لوحة
# محدود نسبيًا (مش نص ضخم زي كتاب كامل)، أضمن حل إننا نخلي
# كل لوحة = وحدة استرجاع واحدة متكاملة.
# ==========================================

# ==========================================
# Embedding Model
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# ==========================================
# Build FAISS
# ==========================================

vector_db = FAISS.from_documents(
    documents,
    embeddings
)

vector_db.save_local(VECTOR_DB_PATH)

print("Vector Database created successfully!")

print(VECTOR_DB_PATH)