import json
import os
import random

CORPUS_FILE = "corpus.json"
OUTPUT_DIR = "dataset"

def load_corpus(filepath):
    """Loads the corpus.json file, skipping comment lines."""
    clean_lines = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("//"):
                continue
            clean_lines.append(line)
    
    # cleaning trailing commas if they exist after comment removal is tricky
    # but since comments were on separate lines and commas are usually after objects,
    # removing the comment line shouldn't break the JSON structure typically found in
    # standard formatted JSON arrays unless the comment was interleaving weirdly.
    # In the file viewed:
    # 18:
    # 19:     // Ini Data Halaman 25.json
    # 20:     {"kata_besemah": "acar", ...
    # The comma from previous object is likely on the line of the previous object (line 17 ended with comma? unseen).
    # Let's check a sample.
    # Line 17: ...},
    # Line 18: 
    # Line 19: // ...
    # Line 20: {...}
    # Removing line 19 leaves: ...}, \n {...} which is valid JSON array.
    
    return json.loads("".join(clean_lines))

def create_instruction_dataset(data):
    """Creates instruction tuning dataset in Alpaca/JSONL format."""
    instructions = []
    
    for item in data:
        k_bes = item.get("kata_besemah", "")
        k_ind = item.get("kata_indonesia", "")
        k_eng = item.get("kata_inggris", "")
        
        kal_bes = item.get("kalimat_besemah", "")
        kal_ind = item.get("kalimat_indonesia", "")
        kal_eng = item.get("kalimat_inggris", "")
        
        # Word Translations
        if k_bes and k_ind:
            instructions.append({
                "instruction": f"Apa arti kata '{k_bes}' dalam Bahasa Indonesia?",
                "input": "",
                "output": k_ind
            })
            instructions.append({
                "instruction": f"Terjemahkan kata '{k_ind}' ke dalam Bahasa Besemah.",
                "input": "",
                "output": k_bes
            })
            
        if k_bes and k_eng:
             instructions.append({
                "instruction": f"Translate the Besemah word '{k_bes}' to English.",
                "input": "",
                "output": k_eng
            })

        # Sentence Translations
        if kal_bes and kal_ind:
             instructions.append({
                "instruction": "Terjemahkan kalimat berikut ke Bahasa Indonesia.",
                "input": kal_bes,
                "output": kal_ind
            })
             instructions.append({
                "instruction": "Terjemahkan kalimat berikut ke Bahasa Besemah.",
                "input": kal_ind,
                "output": kal_bes
            })

        if kal_bes and kal_eng:
             instructions.append({
                "instruction": "Translate this Besemah sentence to English.",
                "input": kal_bes,
                "output": kal_eng
            })

    return instructions

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Loading corpus...")
    try:
        data = load_corpus(CORPUS_FILE)
        print(f"Loaded {len(data)} entries.")
    except Exception as e:
        print(f"Error loading corpus: {e}")
        return

    # 1. Save Clean JSON
    clean_json_path = os.path.join(OUTPUT_DIR, "besemah_dictionary.json")
    with open(clean_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved clean dictionary to {clean_json_path}")

    # 2. Generate Instruction Dataset (JSONL)
    print("Generating instruction dataset...")
    instructions = create_instruction_dataset(data)
    
    # Shuffle
    random.shuffle(instructions)
    
    # Split Train/Val (90/10)
    split_idx = int(len(instructions) * 0.9)
    train_data = instructions[:split_idx]
    val_data = instructions[split_idx:]
    
    train_path = os.path.join(OUTPUT_DIR, "train.jsonl")
    val_path = os.path.join(OUTPUT_DIR, "validation.jsonl")
    
    with open(train_path, 'w', encoding='utf-8') as f:
        for entry in train_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
    with open(val_path, 'w', encoding='utf-8') as f:
        for entry in val_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
    print(f"Saved {len(train_data)} training examples to {train_path}")
    print(f"Saved {len(val_data)} validation examples to {val_path}")
    
    # 3. Create README
    readme_content = f"""# Besemah Language Corpus

This dataset is curated for training and tuning AI models on the Besemah language (South Sumatra, Indonesia).

## Structure

- **besemah_dictionary.json**: The raw dictionary data cleaned of comments.
- **train.jsonl**: Instruction tuning dataset (90% split).
- **validation.jsonl**: Instruction tuning dataset (10% split).

## Statistics

- **Total Entries**: {len(data)}
- **Total Instruction Pairs**: {len(instructions)}
- **Training Examples**: {len(train_data)}
- **Validation Examples**: {len(val_data)}

## Format

The `.jsonl` files follow the Alpaca instruction format:

```json
{{
    "instruction": "...",
    "input": "...",
    "output": "..."
}}
```
"""
    with open(os.path.join(OUTPUT_DIR, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("Created README.md")

if __name__ == "__main__":
    main()
