# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Challenge (June–July) 2026

> 🏆 This repository is my official submission for the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Nesma Nasser Galal                   |
| Project Name     | ArtMuse AI                           |
| GitHub Username  | _NeSma237_                           |
| Challenge Batch  | June–July 2026                       |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en) |

---

# 📖 Project Overview

**ArtMuse AI** is an AI-powered museum docent for the European Paintings collection at The Metropolitan Museum of Art. A visitor uploads a photo of a painting, and the system identifies it using visual embeddings, retrieves verified curatorial information about it (story, symbols, historical context, artist biography, interesting facts), and lets the visitor have a free-form, bilingual (Arabic/English) conversation about the artwork with an AI docent grounded strictly in retrieved facts — no hallucinated art history.

The pipeline runs in four stages, presented in the app as a live "Gallery Map":

```
Room I: Upload  →  Room II: Visual Recognition (CLIP)  →  Room III: Retrieval (FAISS)  →  Room IV: Generation (Mistral)
```

---

# ✨ Features

* **Visual artwork identification** from an uploaded photo using CLIP embeddings, with a confidence threshold to reject unknown images
* **"Similar Artworks" suggestions** based on visual similarity
* **Retrieval-Augmented Generation (RAG)** pipeline using FAISS, with each artwork stored as a single, complete document to avoid losing context across sections
* **Precise ID-based retrieval** (instead of guesswork text similarity) to avoid mixing up visually or thematically similar paintings
* **Bilingual support (Arabic/English)** — the reply language is detected deterministically in Python, not left to the LLM
* **Question-type classification** (artist / symbols / history / biography / facts) to scope the context sent to the model, keeping answers focused
* **Strict anti-hallucination prompting** — the docent answers only from retrieved museum data, and clearly says when information isn't available
* **Structured LLM output** (artwork name, artist, year, answer) via LangChain's output parsers
* **Museum-themed interactive UI** built with Streamlit: magazine-style artwork profile, live gallery-map progress tracker, day/night gallery lighting toggle, suggested questions, and optional voice input/output
* **Developer mode** to inspect the raw retrieved RAG context for debugging

---

# 🛠️ Technologies Used

* **Python 3.12**
* **LangChain** (`langchain`, `langchain-classic`, `langchain-core`, `langchain-community`, `langchain-huggingface`) — orchestration, prompt templates, structured output parsing
* **FAISS** (`faiss-cpu`) — vector database for semantic retrieval
* **Sentence-Transformers** (`paraphrase-multilingual-MiniLM-L12-v2`) — multilingual text embeddings
* **OpenCLIP** (`ViT-B-32`, OpenAI pretrained weights) — image embeddings for visual artwork identification
* **Hugging Face Transformers** + **Mistral-Nemo-Instruct-2407** — the generative LLM (docent)
* **BitsAndBytes / Accelerate** — 4-bit quantization for efficient GPU inference
* **FastAPI** + **Uvicorn** + **ngrok** — backend API serving the LLM, tunneled for external access
* **Streamlit** — frontend web application
* **PIL / NumPy / PyTorch** — image processing and embedding math
* **Metropolitan Museum of Art Collection API** — data source for artworks
* Optional: **SpeechRecognition** (voice input), **gTTS** (voice output)

---

# ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NeSma237/An-AI-Docent-for-the-Galleries.git
   cd An-AI-Docent-for-the-Galleries
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -q transformers sentence-transformers faiss-cpu bitsandbytes accelerate \
       langchain langchain-core langchain-community langchain-huggingface langchain-classic \
       open_clip_torch fastapi uvicorn pyngrok nest_asyncio streamlit pillow numpy torch
   ```

4. Build the data pipeline (run once):
   ```bash
   python collect_ids.py       # collect artwork IDs from the Met API
   python collect.py           # download images + metadata for European Paintings
   python check_duplicates.py  # verify no duplicate IDs
   python clip.py              # build CLIP reference embeddings
   python build_vector_db.py   # build the FAISS vector database
   ```

5. Run the LLM backend (Kaggle/Colab notebook or local GPU machine) to expose the `/generate` endpoint via ngrok, then update `API_URL` in `app.py` with the generated public URL.

---

# 🚀 Usage

1. Launch the app:
   ```bash
   streamlit run app.py
   ```

2. Upload a photo of a European painting from the Met collection.

3. The app will:
   - Identify the artwork (Room II)
   - Retrieve its full curatorial profile (Room III)
   - Display its story, symbols, historical context, artist biography, and interesting facts
   - Suggest similar artworks
   - Let you chat freely with the AI docent about the piece — in Arabic or English

---

# 📸 Demo

![App Screenshot](./screenshots/Screenshot%2026-07-30-073904.png)
![App Screenshot](./screenshots/Screenshot%202026-07-30%20072731.png)

_More screenshots or a short demo video/GIF can be added here — e.g. the identified artwork profile and a sample chat conversation._

---

# 📈 Results

* Curated and cleaned a dataset of **88 unique European Paintings** from the Met Museum collection, each enriched with detailed Arabic curatorial content
* Achieved accurate visual identification via CLIP embeddings with a confidence threshold to filter out unrecognized artworks
* Solved a key RAG accuracy issue by switching from chunked documents to whole-document storage, ensuring no curatorial section (story/symbols/history/etc.) is lost during retrieval
* Delivered a fully bilingual (Arabic/English) conversational experience with deterministic language detection
* Built a polished, museum-themed Streamlit interface with real-time pipeline visualization

---

# 🔮 Future Improvements

* Host the LLM backend permanently instead of relying on temporary ngrok tunnels
* Expand the collection beyond "European Paintings" to other Met Museum departments
* Add real authentication/authorization to the API endpoint
* Summarize conversational memory instead of accumulating full chat history in the prompt
* Add automated evaluation of RAG answer faithfulness

---

# 📚 About the Challenge

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the challenge encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the challenge, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.
