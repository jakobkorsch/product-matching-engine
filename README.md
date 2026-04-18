# 🚀 Product Matching Engine

AI-based product matching engine using semantic similarity and fuzzy matching.

## 💡 Problem
Product data in systems like eCommerce, ERP or PIM is often:
- inconsistent
- unstructured
- difficult to classify

## 🔧 Solution
This project combines:
- Semantic AI (Sentence Transformers)
- Fuzzy Matching (RapidFuzz)
- Custom text preprocessing

## ⚙️ Features
- Top 3 match suggestions
- Hybrid scoring (semantic + fuzzy)
- Works across multiple languages (German & English)
- Excel input & output

## 📊 Example Output

The model can match products even with different descriptions:

- "Edelstahl Schraube M8" → "Schraube aus Edelstahl"
- "Hydraulic pump high pressure" → "Hydraulic pump system"

## ▶️ Usage

```bash
pip install -r requirements.txt
python main.py
