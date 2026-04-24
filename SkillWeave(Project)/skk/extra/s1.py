import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import textwrap

from langdetect import detect
from deep_translator import GoogleTranslator

# IMPORTANT: occupation override (fixes "नाई" issue)
OCCUPATION_MAP = {
    "नाई": "barber",
    "nai": "barber",
    "naayi": "barber",
    "दर्जी": "tailor",
    "darzi": "tailor",
    "किसान": "farmer",
    "kisan": "farmer",
    "मिस्त्री": "mechanic",
    "mistri": "mechanic",
    "मोची": "cobbler",
    "mochi": "cobbler",
    "बढ़ई": "carpenter",
    "badhai": "carpenter",
    "ड्राइवर": "driver",
    "driver": "driver",
    "नर्स": "nurse",
    "मजदूर": "labourer",
    "mazdoor": "labourer"
}

def translate_to_english(text: str) -> str:
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        print(f"🌐 Translated → {translated}")
        return translated.lower()
    except Exception as e:
        print("⚠️ Translation failed:", e)
        return text


def normalize_query(query: str) -> str:
    query = query.strip().lower()

    # ✅ Step 1: occupation dictionary override
    if query in OCCUPATION_MAP:
        print("🧠 Occupation dictionary hit")
        return OCCUPATION_MAP[query]

    # ✅ Step 2: detect language
    try:
        lang = detect(query)
    except Exception:
        return query

    # ✅ Step 3: if already English
    if lang == "en":
        return query

    # ✅ Step 4: translate everything else
    return translate_to_english(query)


# ---------------- CONFIG ----------------

INDEX_PATH = "skillweave.index"
DATA_PATH = "data/skillweave_clean.csv"
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

TOP_K = 5
FAISS_K = 50

SEMANTIC_WEIGHT = 0.99
KEYWORD_WEIGHT = 0.01

# ---------------------------------------

def load_resources():
    print("🔹 Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("🔹 Loading FAISS index...")
    index = faiss.read_index(INDEX_PATH)

    print("🔹 Loading metadata...")
    df = pd.read_csv(DATA_PATH, low_memory=False)

    for col in df.columns:
        df[col] = df[col].fillna("")

    return model, index, df


def embed_query(model, query: str) -> np.ndarray:
    emb = model.encode([query], normalize_embeddings=True)
    return emb.astype("float32")


def keyword_overlap_score(query: str, text: str) -> float:
    q_words = set(query.lower().split())
    t_words = set(text.lower().split())

    if not q_words:
        return 0.0

    return len(q_words & t_words) / len(q_words)


def search(query, model, index, df):
    query_emb = embed_query(model, query)
    scores, indices = index.search(query_emb, FAISS_K)

    results = []
    for rank, idx in enumerate(indices[0]):
        row = df.iloc[idx]

        semantic_score = float(scores[0][rank])

        title_kw = keyword_overlap_score(query, row["title"])
        desc_kw = keyword_overlap_score(query, row["description"])
        keyword_score = (0.7 * title_kw) + (0.3 * desc_kw)

        final_score = (
            SEMANTIC_WEIGHT * semantic_score +
            KEYWORD_WEIGHT * keyword_score
        )

        results.append({
            "nco_code": row["nco_code_2015"],
            "title": row["title"],
            "division": row["division_name"],
            "sub_division": row["sub_division_name"],
            "description": row["description"],
            "score": final_score,
            "semantic": semantic_score,
            "keyword": keyword_score
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:TOP_K]


def print_results(query, results):
    print("\nTop Matches for:", query)
    print("=" * 60)

    for r in results:
        print(f"NCO Code : {r['nco_code']}")
        print(f"Title    : {r['title']}")
        print(f"Division : {r['division']} → {r['sub_division']}")
        print(f"Score    : {r['score']:.4f}")
        print(
            f"Reason   : Semantic ({r['semantic']:.3f}) "
            f"+ Keyword ({r['keyword']:.3f})"
        )

        desc = textwrap.shorten(
            r["description"],
            width=220,
            placeholder="..."
        )
        print(f"Desc     : {desc}")
        print("-" * 60)


def main():
    model, index, df = load_resources()

    while True:
        query = input("\nEnter job search query (or type 'exit'): ").strip()
        if query.lower() == "exit":
            break

        query = normalize_query(query)
        print("🔍 Final Query Used:", query)

        results = search(query, model, index, df)
        print_results(query, results)


# API hook
def search_api(query: str, top_k: int = 5):
    model, index, df = load_resources()

    query = normalize_query(query)
    results = search(query, model, index, df)

    return [{
        "nco_code": r["nco_code"],
        "title": r["title"],
        "division": f'{r["division"]} → {r["sub_division"]}',
        "description": r["description"],
        "score": round(float(r["score"]), 3)
    } for r in results[:top_k]]


if __name__ == "__main__":
    main()