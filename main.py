import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util
from rapidfuzz import fuzz

# ---------------------------
# 1. MODEL LADEN
# ---------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

# ---------------------------
# 2. TEXT CLEANING
# ---------------------------
def clean_text(s):
    s = str(s).lower()
    s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r'\d+', ' ', s)
    s = re.sub(r'[^\w\s]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

# ---------------------------
# 3. DATEN LADEN
# ---------------------------
df_source = pd.read_excel("sample_input.xlsx")
df_ref = pd.read_excel("sample_reference.xlsx")

df_source["clean"] = df_source["text"].apply(clean_text)
df_ref["clean"] = df_ref["text"].apply(clean_text)

# ---------------------------
# 4. EMBEDDINGS
# ---------------------------
emb_ref = model.encode(df_ref["clean"].tolist(), convert_to_tensor=True)

# ---------------------------
# 5. MATCHING FUNCTION
# ---------------------------
def hybrid_match(query, top_k=3):
    emb_q = model.encode([query], convert_to_tensor=True)
    cos_scores = util.cos_sim(emb_q, emb_ref)[0]

    results = []

    for i, score in enumerate(cos_scores):
        semantic_score = float(score)
        fuzzy_score = fuzz.ratio(query, df_ref.iloc[i]["clean"]) / 100

        final_score = 0.7 * semantic_score + 0.3 * fuzzy_score

        results.append({
            "match": df_ref.iloc[i]["text"],
            "score_raw": final_score,  # wichtig für Sortierung
            "score": f"{int(final_score * 100)}%"  # Anzeige
        })

    # RICHTIG sortieren (nach numeric score)
    results = sorted(results, key=lambda x: x["score_raw"], reverse=True)

    # Nur Top-K zurückgeben (ohne score_raw)
    return [
        {"match": r["match"], "score": r["score"]}
        for r in results[:top_k]
    ]

# ---------------------------
# 6. MATCHING AUSFÜHREN
# ---------------------------
output = []

for _, row in df_source.iterrows():
    matches = hybrid_match(row["clean"])

    for m in matches:
        output.append({
            "input": row["text"],
            "match": m["match"],
            "score": m["score"]
        })

# ---------------------------
# 7. ERGEBNIS SPEICHERN
# ---------------------------
df_out = pd.DataFrame(output)
df_out.to_excel("results.xlsx", index=False)

print("✅ Matching abgeschlossen! Datei: results.xlsx")