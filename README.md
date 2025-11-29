🍳 AI Chef Pro — AI-Powered Culinary Assistant
---

AI Chef Pro is a local-first, privacy-focused Generative AI application that helps you turn everyday ingredients into chef-quality recipes. It combines Computer Vision, RAG (Retrieval-Augmented Generation), and local LLM inference to reduce food waste and inspire smarter home cooking.

🔗 **Live Demo:**  

[Watch on YouTube](https://www.youtube.com/watch?v=RlrUmQEKPLs)



 

🚀 Key Features
---

*   👁️ **Multi-Modal Perception**  
    Uses CLIP for semantic ingredient detection and Tesseract OCR for reading packaged food labels.
*   🧠 **Local LLM Inference (CPU-Only)**  
    Runs a quantized 7B model via `llama.cpp` with `llama-cpp-python`. No GPU required.
*   📚 **RAG with ChromaDB**  
    Retrieves context from curated recipes to keep outputs grounded.
*   👨‍🍳 **Structured Recipe Output**  
    Professional formatting with titles, descriptions, steps, and chef tips.
*   ✏️ **Human-in-the-Loop Editing**  
    Users can adjust detected ingredients before recipe generation.

 

🧱 Tech Stack
---

*   **Frontend:** Streamlit
*   **LLM Inference:** llama-cpp-python (GGUF)
*   **Vector Store:** ChromaDB
*   **Embeddings:** all-MiniLM-L6-v2
*   **Vision:** CLIP + Tesseract OCR
*   **Image Processing:** Pillow
*   **Language:** Python 3.9+

 

📂 Project Structure
---

    AI-chef-pro/
    ├── app.py                   # Streamlit UI entry point
    ├── backend/
    │   ├── config.py            # Global configurations
    │   ├── detection.py         # CLIP + OCR ingredient 
    │   ├── retrieval.py         # ChromaDB RAG logic
    │   ├── llm.py               # Llama.cpp model loader
    │   └── recipe_generator.py  # Prompting response formatting
    ├── seed_data/
    │   └── indian_recipes.jsonl # RAG dataset
    ├── scripts/
    │   └── seed_chroma.py       # One-time DB seeding script
    ├── models.gguf              # Quantized LLM model 
    ├── packages.txt             # System deps for Spaces 
    ├── requirements.txt         # Python dependencies
    └── README.md                # Project documentation
    

_Note:_ `models.gguf` should be kept local or uploaded manually to Hugging Face Spaces — it is not committed to Git.

 

💻 Local Setup — Step-by-Step
---

### 1\. Prerequisites

*   Python **3.9+**
*   Git
*   **Tesseract OCR** installed and available in PATH

### Install Tesseract

**Windows:** Download from the official installer

**macOS:**

    brew install tesseract
    

**Linux (Debian/Ubuntu):**

    sudo apt-get update
    sudo apt-get install tesseract-ocr
    

 

### 2\. Clone the Repository

    git clone https://github.com/YourUsername/AI-chef-pro.git
    cd AI-chef-pro
    

Replace `YourUsername` with your GitHub username.

 

### 3\. Create & Activate Virtual Environment

    python -m venv venv
    
    # Windows:
    venv\Scripts\activate
    
    # macOS / Linux:
    source venv/bin/activate
    

 

### 4\. Install Python Dependencies

    pip install -r requirements.txt
    

 

### 5\. Download & Place the GGUF Model

Download a GGUF model such as `Mistral-7B-Instruct-v0.1.Q4_K_M.gguf`.

Rename it to:

    models.gguf
    

Place it in the project root.

 

### 6\. Seed the Vector Database (Optional)

    python scripts/seed_chroma.py
    

The app may auto-seed on first run.

 

### 7\. Run the Streamlit App

    streamlit run app.py
    

Visit **http://localhost:8501** to open the app.

You can now:

*   Upload ingredient images
*   Edit detected ingredients
*   Generate chef-style recipes

 

☁️ Deploying to Hugging Face Spaces
-----------------------------------

### 1\. Create a New Space

*   Go to Hugging Face → Spaces → New Space
*   Select **Streamlit**
*   Name: `AI-chef-pro`

### 2\. Push Code to the Space

    git remote add hf https://huggingface.co/spaces/USERNAME/AI-chef-pro
    git push hf main
    

Replace `USERNAME` with your HF username.

### Ensure `.gitignore` contains:

    models.gguf
    chroma_db/
    __pycache__/
    .venv/
    

### 3\. Upload the Model Separately

*   Go to Files tab → Add file → Upload
*   Upload `models.gguf`
*   Ensure it appears in the root

### 4\. Build & Run

*   `packages.txt` installs Tesseract
*   `requirements.txt` installs Python deps

When the Space shows **Running**, the app is live.



👨‍💻 Author
------------

**Created by:**  
**Sarvesh Talele** — AI Engineer & builder of practical, local-first AI tools.

If you use or extend this project, please star the repo or mention it on LinkedIn.
