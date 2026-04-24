# search.py
# SkillWeave Semantic Search (Multilingual + Hinglish + Boosted Ranking)

import faiss
import pandas as pd
import numpy as np
import unicodedata
import textwrap
from sentence_transformers import SentenceTransformer

# ---------------- CONFIG ----------------

INDEX_PATH = "skillweave.index"
DATA_PATH = "data/skillweave_clean.csv"

MODEL_NAME = "intfloat/multilingual-e5-large"

TOP_K = 5
FAISS_K = 50

SEMANTIC_WEIGHT = 0.8
KEYWORD_WEIGHT = 0.2

# ---------------- HINGLISH MAP ----------------

HINGLISH_MAP = {
    "kisan": "farmer",
    "dudhwala": "milk seller",
    "sabziwala": "vegetable seller",
    "mazdoor": "labourer",
    "darzi": "tailor",
    "nai": "barber",
    "mistri": "mechanic",
    "mochi": "cobbler",
    "badhai": "carpenter",
    "kumhar": "potter",
    "lohar": "blacksmith"
}

# ---------------- SYNONYMS ----------------

SYNONYMS = {
    "farmer": ["cultivator", "agricultural worker"],
    "driver": ["vehicle driver", "truck driver"],
    "labourer": ["construction worker", "manual worker"],
    "mechanic": ["repair worker", "technician"]
}

# ---------------- QUERY NORMALIZATION ----------------

def normalize_query(query):
    query = query.strip().lower()

    # normalize unicode
    query = unicodedata.normalize("NFKC", query)

    words = query.split()

    # Hinglish conversion
    words = [HINGLISH_MAP.get(w, w) for w in words]

    query = " ".join(words)

    # synonym expansion
    expanded_words = query.split()

    for word in expanded_words:
        if word in SYNONYMS:
            query += " " + " ".join(SYNONYMS[word])

    return query


# ---------------- LOAD RESOURCES ----------------

def load_resources():
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Loading FAISS index...")
    index = faiss.read_index(INDEX_PATH)

    print("Loading metadata...")
    df = pd.read_csv(DATA_PATH)

    df = df.fillna("")

    return model, index, df


# ---------------- EMBEDDING ----------------

def embed_query(model, query):
    prefixed = "query: " + query
    emb = model.encode([prefixed], normalize_embeddings=True)
    return emb.astype("float32")


# ---------------- KEYWORD OVERLAP ----------------

def keyword_overlap(query, text):

    q_words = set(query.lower().split())
    t_words = set(text.lower().split())

    if len(q_words) == 0:
        return 0.0

    return len(q_words & t_words) / len(q_words)


# ---------------- SEARCH ----------------

def search(query, model, index, df):

    query_emb = embed_query(model, query)

    scores, indices = index.search(query_emb, FAISS_K)

    results = []

    for rank, idx in enumerate(indices[0]):

        if idx == -1:
            continue

        row = df.iloc[idx]

        semantic_score = float(scores[0][rank])

        title = str(row.get("title", ""))
        desc = str(row.get("description", ""))

        title_kw = keyword_overlap(query, title)
        desc_kw = keyword_overlap(query, desc)

        keyword_score = 0.7 * title_kw + 0.3 * desc_kw

        # TITLE BOOST
        title_boost = 0.0
        if query.split()[0] in title.lower():
            title_boost = 0.15

        # DIVISION BOOST
        division_boost = 0.0
        division_name = str(row.get("division_name", "")).lower()
        if query.split()[0] in division_name:
            division_boost = 0.05

        final_score = (
            SEMANTIC_WEIGHT * semantic_score
            + KEYWORD_WEIGHT * keyword_score
            + title_boost
            + division_boost
        )

        results.append({
            "nco_code": row.get("nco_code_2015", ""),
            "title": title,
            "division": row.get("division_name", ""),
            "sub_division": row.get("sub_division_name", ""),
            "description": desc,
            "score": final_score
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:TOP_K]


# ---------------- PRINT RESULTS ----------------

def print_results(query, results):

    print("\nTop Matches for:", query)
    print("=" * 60)

    for r in results:

        print("NCO Code :", r["nco_code"])
        print("Title    :", r["title"])
        print("Division :", r["division"], "→", r["sub_division"])
        print("Score    :", round(r["score"], 4))

        desc = textwrap.shorten(
            r["description"],
            width=200,
            placeholder="..."
        )

        print("Desc     :", desc)
        print("-" * 60)


# ---------------- MAIN LOOP ----------------

def main():

    model, index, df = load_resources()

    while True:

        query = input("\nEnter job query (or 'exit'): ")

        if query.lower() == "exit":
            break

        normalized = normalize_query(query)

        if normalized != query:
            print("Normalized query →", normalized)

        results = search(normalized, model, index, df)

        print_results(normalized, results)


# ---------------- RUN ----------------

if __name__ == "__main__":
    main()