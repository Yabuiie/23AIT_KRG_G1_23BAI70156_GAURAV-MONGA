import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import textwrap

# ---------------- CONFIG ----------------

INDEX_PATH = "skillweave.index"
DATA_PATH = "data/skillweave_clean.csv"
MODEL_NAME = "intfloat/multilingual-e5-base"

TOP_K = 5
FAISS_K = 50

# ---------------------------------------


# 🔥 Hinglish + regional mapping
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


# ---------------- QUERY LOGIC ----------------

def normalize_query(query: str) -> str:
    query = query.strip().lower()

    if query in OCCUPATION_MAP:
        print("🧠 Occupation dictionary hit")
        query = OCCUPATION_MAP[query]

    # E5 requires prefix
    return "query: " + query


def is_general_query(query: str) -> bool:
    clean_query = query.replace("query:", "").strip()
    words = clean_query.split()

    return len(words) <= 2


# ---------------- SCORING ----------------

def generality_score(title: str) -> float:
    words = title.lower().split()

    # fewer words → more general
    return 1 / (len(words) + 1)


def keyword_overlap_score(query: str, text: str):
    q_words = set(query.replace("query:", "").split())
    t_words = set(text.lower().split())

    if not q_words:
        return 0.0

    return len(q_words & t_words) / len(q_words)


# ---------------- LOAD ----------------

def load_resources():
    print("🔹 Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    print("🔹 Loading index...")
    index = faiss.read_index(INDEX_PATH)

    print("🔹 Loading metadata...")
    df = pd.read_csv(DATA_PATH)

    for col in df.columns:
        df[col] = df[col].fillna("")

    return model, index, df


def embed_query(model, query: str):
    emb = model.encode([query], normalize_embeddings=True)
    return emb.astype("float32")


# ---------------- SEARCH CORE ----------------

def search(query, model, index, df):
    query_emb = embed_query(model, query)
    scores, indices = index.search(query_emb, FAISS_K)

    results = []
    general_query_flag = is_general_query(query)

    for rank, idx in enumerate(indices[0]):
        row = df.iloc[idx]

        semantic_score = float(scores[0][rank])

        # keyword score
        title_kw = keyword_overlap_score(query, row["title"])
        desc_kw = keyword_overlap_score(query, row["description"])
        keyword_score = (0.7 * title_kw) + (0.3 * desc_kw)

        # generality score
        gen_score = generality_score(row["title"])

        # exact match bonus
        clean_query = query.replace("query:", "").strip()
        exact_match_bonus = 0
        if clean_query in row["title"].lower():
            exact_match_bonus = 0.2

        # 🔥 FINAL RANKING LOGIC
        if general_query_flag:
            final_score = (
                0.75 * semantic_score +
                0.1 * keyword_score +
                0.15 * gen_score
            )
        else:
            final_score = (
                0.9 * semantic_score +
                0.1 * keyword_score
            )

        final_score += exact_match_bonus

        results.append({
            "nco_code": row["nco_code_2015"],
            "title": row["title"],
            "division": row["division_name"],
            "sub_division": row["sub_division_name"],
            "description": row["description"],
            "score": final_score,
            "semantic": semantic_score,
            "keyword": keyword_score,
            "generality": gen_score
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:TOP_K]


# ---------------- OUTPUT ----------------

def print_results(query, results):
    print("\nTop Matches for:", query)
    print("=" * 60)

    for r in results:
        print(f"NCO Code : {r['nco_code']}")
        print(f"Title    : {r['title']}")
        print(f"Division : {r['division']} → {r['sub_division']}")
        print(f"Score    : {r['score']:.4f}")
        print(
            f"Reason   : Semantic({r['semantic']:.3f}) | "
            f"Keyword({r['keyword']:.3f}) | "
            f"General({r['generality']:.3f})"
        )

        desc = textwrap.shorten(
            r["description"],
            width=220,
            placeholder="..."
        )
        print(f"Desc     : {desc}")
        print("-" * 60)


# ---------------- MAIN ----------------

def main():
    model, index, df = load_resources()

    while True:
        query = input("\nEnter job search query (or type 'exit'): ").strip()
        if query.lower() == "exit":
            break

        query = normalize_query(query)
        print("🔍 Final Query:", query)

        results = search(query, model, index, df)
        print_results(query, results)


if __name__ == "__main__":
    main()