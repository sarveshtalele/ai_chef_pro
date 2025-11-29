# Pantry Chef — Light (Hugging Face Space optimized)

Pantry Chef is a lightweight, local-first recipe generator: upload a photo of your pantry or type ingredients and get **three practical recipe options**. This Light version is optimized for Hugging Face Spaces (free CPU) and uses OCR, semantic embedding mapping, Chroma for RAG, and a local GGUF model via `llama.cpp`.

---

## Features

- Lightweight ingredient detection (OCR + embeddings)
- Ingredient normalization (sentence-transformers)
- Retrieval-Augmented Generation with Chroma DB (local recipe retrieval)
- LLM generation using a local GGUF model via `llama-cpp-python`
- Minimal iOS-inspired white & yellow Streamlit UI
- Scripted seeding of Chroma with sample Indian recipes

---

## Repo Layout

```
pantry-chef-light/
├── app.py
├── backend/
│ ├── config.py
│ ├── detection.py
│ ├── retrieval.py
│ ├── llm.py
│ └── recipe.py
├── seed_data/indian_recipes.jsonl
├── scripts/seed_chroma.py
├── requirements.txt
├── packages.txt
├── models.gguf
└── README.md
```
