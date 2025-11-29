import json
import os
import sys

# 1. Setup paths to allow importing from 'backend'
# Current script location: /pantry-chef-light/scripts/
HERE = os.path.dirname(os.path.abspath(__file__))
# Root location: /pantry-chef-light/
ROOT = os.path.dirname(HERE)
sys.path.append(ROOT)

from backend.rag_pipeline import add_recipe

# Path to the data file
DATA_FILE = os.path.join(ROOT, "seed_data", "indian_recipes.jsonl")

def seed():
    # Check if file exists
    if not os.path.exists(DATA_FILE):
        print(f"❌ Error: Data file not found at: {DATA_FILE}")
        print("Please ensure 'indian_recipes.jsonl' is inside the 'seed_data' folder.")
        return

    print(f"🌱 Reading recipes from: {DATA_FILE}")
    print("⏳ Seeding ChromaDB...")
    
    count = 0
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    obj = json.loads(line)
                    
                    # Extract fields with fail-safes
                    # Use provided ID, or generate one from title if missing
                    title = obj.get("title", "Untitled Recipe")
                    rid = str(obj.get("id") or title[:12].replace(" ", "_"))
                    
                    # Some datasets use 'text' others use 'instructions'
                    text = obj.get("text") or obj.get("instructions") or ""
                    
                    ingredients = obj.get("ingredients", [])
                    
                    # Only add if valid data exists
                    if text:
                        add_recipe(rid, title, text, ingredients)
                        print(f"  + Added: {title}")
                        count += 1
                        
                except json.JSONDecodeError:
                    print(f"  ⚠️ Skipping invalid JSON line")
                except Exception as e:
                    print(f"  ⚠️ Error adding line: {e}")

    except Exception as e:
        print(f"critical error reading file: {e}")

    print(f"✅ Seeding Complete. Total recipes indexed: {count}")

if __name__ == "__main__":
    seed()