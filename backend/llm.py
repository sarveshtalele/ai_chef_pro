import os
import logging
import multiprocessing
from .config import MODEL_PATH

logger = logging.getLogger(__name__)
_llm_instance = None

def load_llm():
    """Loads the GGUF model with optimal CPU settings."""
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please upload model.gguf.")

    try:
        from llama_cpp import Llama
        
        # CPU Optimization
        cores = multiprocessing.cpu_count()
        
        logger.info(f"Loading Llama model on {cores} threads...")
        _llm_instance = Llama(
            model_path=MODEL_PATH,
            n_ctx=2048,      # Context window
            n_gpu_layers=0,  # Force CPU
            n_threads=cores, # Maximize CPU usage
            verbose=False
        )
        return _llm_instance
    except Exception as e:
        logger.error(f"LLM Load Failed: {e}")
        return None

def generate_text(prompt: str, max_tokens: int = 1024) -> str:
    llm = load_llm()
    if not llm:
        return "System Error: Model could not be loaded."

    # Mistral/Llama Instruction Format
    formatted = f"[INST] {prompt} [/INST]"
    
    output = llm.create_completion(
        prompt=formatted,
        max_tokens=max_tokens,
        temperature=0.7,
        top_p=0.9,
        stop=["[INST]", "User:"],
        echo=False
    )
    return output['choices'][0]['text'].strip()