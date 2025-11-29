import os

# Path to the GGUF model.
# Ensure 'model.gguf' is present in the root directory.
MODEL_PATH = os.getenv("HF_GGUF_MODEL_PATH", "model.gguf")

# Persistence directory for the Vector Database
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")

# Embedding model for RAG (Small and fast for CPU)
EMBED_MODEL = "all-MiniLM-L6-v2"

# Collection name for recipes
COLLECTION_NAME = "recipes"