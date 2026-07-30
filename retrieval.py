import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DB_PATH = os.path.join(BASE_DIR, "data", "vector_db")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

db = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

# ==========================================
# فهرس id -> Document
#
# بدل ما ندور بالـ similarity_search (بحث تخميني بالمعنى النصي)،
# بما إن identify_artwork بيرجع الـ id الدقيق للوحة من CLIP،
# أضمن حل إننا نجيب الـ Document المطابق تمامًا بالـ id، مباشرة
# من الـ docstore، من غير أي احتمال غلط أو خلط بين لوحتين
# بأسماء متشابهة (زي "Virgin and Child" اللي عندنا منها أكتر من نسخة).
# ==========================================

_id_index = {
    doc.metadata.get("id"): doc
    for doc in db.docstore._dict.values()
}


def retrieve_context(artwork_id=None, artwork_name=None):
    """
    الاستخدام المفضل: retrieve_context(artwork_id=...)
    بيرجع الـ Document المطابق تمامًا بالـ id، من غير أي بحث تخميني.

    لو اتبعت artwork_name بس (بدون id) - بيرجع لطريقة similarity_search
    القديمة كـ fallback، لكنها أقل دقة وممكن تجيب لوحة غلط لو الأسماء متشابهة.
    """

    if artwork_id is not None:
        doc = _id_index.get(artwork_id)
        if doc is not None:
            return doc
        # لو الـ id مش موجود في الفهرس (نادر)، نكمل على fallback بالاسم لو موجود

    if artwork_name is not None:
        docs = db.similarity_search(artwork_name, k=1)
        if docs:
            return docs[0]

    return None

import re

def detect_question_type(question):

    q = question.lower()

    # Artist
    if any(x in q for x in [
        "artist",
        "who painted",
        "who made",
        "painted by"
    ]):
        return "artist"

    if re.search(r"(الفنان|الرسام|مين رسم|من رسم|رسمها مين)", question):
        return "artist"

    # Symbols
    if any(x in q for x in [
        "symbol",
        "symbols",
        "meaning",
        "represent"
    ]):
        return "symbols"

    if re.search(r"(رمز|يرمز|معنى|الرموز)", question):
        return "symbols"

    # History
    if any(x in q for x in [
        "history",
        "historical",
        "why important",
        "significant",
        "when"
    ]):
        return "history"

    if re.search(r"(تاريخ|الخلفية|متى|امتى|أهمية|مهم)", question):
        return "history"

    # Biography
    if any(x in q for x in [
        "biography",
        "about the artist"
    ]):
        return "biography"

    if re.search(r"(احكيلي عن الفنان|عن الفنان|السيرة الذاتية)", question):
        return "biography"

    # Interesting Facts
    if any(x in q for x in [
        "interesting",
        "fact",
        "fun fact"
    ]):
        return "facts"

    if re.search(r"(حقائق|معلومة|شيقة)", question):
        return "facts"

    return "general"

SECTION_HEADERS = [
    "Artwork Name:",
    "Artist:",
    "Year:",
    "Style:",
    "Department:",
    "Materials:",
    "Story:",
    "Symbols:",
    "Artist Biography:",
    "Historical Context:",
    "Interesting Facts:",
]

def extract_section(text, header):

    lines = text.splitlines()

    capture = False

    result = []

    for line in lines:

        stripped = line.strip()

        if stripped == header.strip():

            capture = True

            result.append(line)

            continue

        if capture:

            # نوقف الالتقاط بس لو السطر ده فعلاً عنوان قسم تاني معروف،
            # مش أي سطر فيه ':' بالصدفة (زي اقتباس أو تاريخ جوه المحتوى نفسه)
            if stripped in SECTION_HEADERS:

                break

            result.append(line)

    return "\n".join(result)

def build_context(doc, question):

    text = doc.page_content

    qtype = detect_question_type(question)

    sections = []

    # دائما ضيف اسم اللوحة
    sections.append(extract_section(text, "Artwork Name:"))

    if qtype == "artist":

        sections.append(extract_section(text, "Artist:"))
        sections.append(extract_section(text, "Artist Biography:"))

    elif qtype == "symbols":

        sections.append(extract_section(text, "Story:"))
        sections.append(extract_section(text, "Symbols:"))

    elif qtype == "history":

        sections.append(extract_section(text, "Year:"))
        sections.append(extract_section(text, "Historical Context:"))

    elif qtype == "facts":

        sections.append(extract_section(text, "Interesting Facts:"))

    elif qtype == "biography":

        sections.append(extract_section(text, "Artist Biography:"))

    else:

        sections.append(extract_section(text, "Artist:"))
        sections.append(extract_section(text, "Year:"))
        sections.append(extract_section(text, "Story:"))
        sections.append(extract_section(text, "Symbols:"))
        sections.append(extract_section(text, "Historical Context:"))
        sections.append(extract_section(text, "Interesting Facts:"))

    return "\n\n".join(
        section for section in sections if section.strip()
    )