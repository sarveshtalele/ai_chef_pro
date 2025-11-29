from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer
from .config import CHROMA_DIR, EMBED_MODEL, COLLECTION_NAME

_embedding_model = None
_client = None
_collection = None

def _get_resources():
    """Lazy loader for Database resources."""
    global _embedding_model, _client, _collection
    
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBED_MODEL)
    
    if _client is None:
        # PersistentClient ensures data is saved to disk
        _client = chromadb.PersistentClient(path=CHROMA_DIR)
    
    if _collection is None:
        _collection = _client.get_or_create_collection(name=COLLECTION_NAME)
            
    return _embedding_model, _collection

def add_recipe(rid: str, title: str, text: str, ingredients: List[str]):
    """Adds a verified recipe to the vector store."""
    emb_model, col = _get_resources()
    
    # Create a rich semantic string for embedding
    semantic_string = f"{title} | Ingredients: {', '.join(ingredients)}"
    vector = emb_model.encode([semantic_string], convert_to_numpy=True)[0].tolist()
    
    col.add(
        ids=[str(rid)],
        documents=[text],
        metadatas=[{"title": title, "ingredients": ", ".join(ingredients)}],
        embeddings=[vector]
    )

def query_similar(ingredients: List[str], top_k: int = 2) -> List[Dict]:
    """Finds recipes in the DB that match the input ingredients."""
    emb_model, col = _get_resources()
    
    query_text = "Recipes containing: " + ", ".join(ingredients)
    query_vec = emb_model.encode([query_text], convert_to_numpy=True)[0].tolist()
    
    results = col.query(
        query_embeddings=[query_vec], 
        n_results=top_k,
        include=['metadatas', 'documents', 'distances']
    )
    
    out = []
    if results and results['ids']:
        for i in range(len(results['ids'][0])):
            meta = results['metadatas'][0][i]
            out.append({
                "id": results['ids'][0][i],
                "score": results['distances'][0][i],
                "title": meta.get("title", "Unknown"),
                "ingredients": meta.get("ingredients", ""),
                "recipe_text": results['documents'][0][i]
            })
    return out