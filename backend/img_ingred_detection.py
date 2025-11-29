import io
import logging
from typing import List, Set
from PIL import Image, ImageEnhance


# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- IMPORTS & FALLBACKS ---
try:
    import pytesseract
except ImportError:
    pytesseract = None
    logger.warning("pytesseract not found. OCR disabled.")

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    SentenceTransformer = None
    logger.error("sentence-transformers not found.")

# --- KNOWLEDGE BASE (Expanded) ---
VOCAB_CATEGORIES = {
    "Produce": [
        "tomato", "onion", "garlic", "ginger", "potato", "carrot", 
        "cucumber", "broccoli", "cauliflower", "spinach", "cabbage",
        "lettuce", "bell pepper", "green chili", "red chili", "mushroom", 
        "zucchini", "eggplant", "pumpkin", "green beans", "lemon", "lime",
        "avocado", "corn", "peas", "cilantro", "parsley", "basil"
    ],
    "Proteins": [
        "chicken", "chicken breast", "ground beef", "pork", "fish", "salmon", 
        "tuna", "shrimp", "egg", "tofu", "paneer", "lentils", "chickpeas", 
        "black beans", "kidney beans"
    ],
    "Pantry & Dairy": [
        "rice", "basmati rice", "pasta", "spaghetti", "macaroni", "bread", 
        "flour", "sugar", "salt", "pepper", "oil", "olive oil", "soy sauce",
        "vinegar", "cheese", "cheddar", "mozzarella", "milk", "butter", 
        "yogurt", "cream", "mayonnaise", "ketchup", "mustard"
    ]
}

# Flatten vocab list for the model
VOCAB = [item for sublist in VOCAB_CATEGORIES.values() for item in sublist]

# Synonyms to normalize outputs
SYNONYMS = {
    "capsicum": "bell pepper",
    "tomatoes": "tomato",
    "potatoes": "potato",
    "chilies": "chili",
    "aubergine": "eggplant",
    "coriander": "cilantro",
    "eggs": "egg"
}

_clip_model = None
_vocab_embeddings = None

def load_clip_model():
    """Singleton loader for CLIP."""
    global _clip_model, _vocab_embeddings
    
    if _clip_model is None and SentenceTransformer is not None:
        logger.info("Loading CLIP model...")
        _clip_model = SentenceTransformer('clip-ViT-B-32')
        _vocab_embeddings = _clip_model.encode(VOCAB, convert_to_tensor=True)
    
    return _clip_model, _vocab_embeddings

def visual_detect(image: Image.Image, threshold: float = 0.22) -> Set[str]:
    """
    Detects objects using CLIP with a lowered threshold for better sensitivity.
    """
    model, vocab_emb = load_clip_model()
    if model is None: return set()

    # Encode image
    image_emb = model.encode(image, convert_to_tensor=True)
    
    # Calculate similarity
    cosine_scores = util.cos_sim(image_emb, vocab_emb)[0]

    found = set()
    # Get top matches, not just threshold
    # We use a loop to check threshold to allow multiple items
    for idx, score in enumerate(cosine_scores):
        if score > threshold:
            item = VOCAB[idx]
            found.add(item)
            
    return found

def ocr_detect(image: Image.Image) -> Set[str]:
    """
    Detects text. Includes image preprocessing to read blurry labels better.
    """
    if pytesseract is None: return set()
    
    try:
        # Preprocessing: Increase contrast for better text reading
        enhancer = ImageEnhance.Contrast(image)
        enhanced_img = enhancer.enhance(1.8) # Increase contrast
        
        # Run OCR
        text = pytesseract.image_to_string(enhanced_img).lower()
        
        # Simple keyword matching against our Vocab
        found = set()
        for v in VOCAB:
            # Check if the vocab word is in the text (e.g., "barilla pasta" -> "pasta")
            # We add spaces to avoid partial matches like "rice" in "price"
            if f" {v} " in f" {text} " or v in text.split():
                found.add(v)
        return found
    except Exception as e:
        logger.warning(f"OCR Error: {e}")
        return set()

def extract_ingredients(image_bytes: bytes) -> List[str]:
    """
    Combines Visual + OCR and normalizes results.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        logger.error(f"Image load error: {e}")
        return []

    detected = set()
    
    # 1. Visual Detection (Vegetables/Fruits)
    detected.update(visual_detect(image))
    
    # 2. OCR Detection (Packaged Goods)
    detected.update(ocr_detect(image))

    # 3. Normalization
    final_list = []
    for item in detected:
        # Map synonyms (e.g., capsicum -> bell pepper)
        normalized = SYNONYMS.get(item, item)
        final_list.append(normalized)

    # Return unique sorted list
    return sorted(list(set(final_list)))