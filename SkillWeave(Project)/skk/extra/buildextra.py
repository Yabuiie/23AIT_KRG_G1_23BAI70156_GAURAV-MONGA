# build_index.py
# SkillWeave – Semantic Index Builder (Multilingual SentenceTransformer)

import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os

# ---------------- CONFIG ----------------
DATA_PATH = "data/skillweave_clean.csv"
INDEX_PATH = "skillweave.index"
META_PATH = "skillweave_metadata.csv"

# Upgraded: multilingual model supporting Hindi, Hinglish (after transliteration),
# Tamil, Telugu, Bengali, Marathi, and 90+ other languages
MODEL_NAME = "intfloat/multilingual-e5-large"

BATCH_SIZE = 32          # slightly smaller — this model is heavier than mpnet
TOP_TEXT_LEN = 1200      # avoid extremely long rows
# ---------------------------------------


def build_semantic_text(row):
    """
    Create a rich semantic representation for each occupation.
    IMPORTANT: For multilingual-e5, documents must be prefixed with "passage: "
    This is how the model was trained — it expects this prefix for indexed content.
    """
    parts = [
        f"Job Title: {row['title']}",
        f"Description: {row['description']}",
        f"Division: {row['division_name']}",
        f"Sub Division: {row['sub_division_name']}",
        f"Group: {row['group_name']}",
        f"Family: {row['family_name']}",
    ]

    text = ". ".join([p for p in parts if isinstance(p, str)])
    text = text[:TOP_TEXT_LEN]

    # ✅ Required prefix for multilingual-e5 passage/document encoding
    return f"passage: {text}"


def main():
    print("📄 Loading dataset...")
    df = pd.read_csv(DATA_PATH, dtype=str, keep_default_na=False)
    print(f"✅ Rows loaded: {len(df)}")

    print("🧠 Building semantic text...")
    df["semantic_text"] = df.apply(build_semantic_text, axis=1)

    texts = df["semantic_text"].tolist()

    print("🤖 Loading multilingual-e5-large model...")
    print("   ⚠️  First run will download ~2.2GB model weights")
    model = SentenceTransformer(MODEL_NAME)

    print("⚙️  Creating embeddings (batched)...")
    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True   # cosine similarity ready
    )

    print("📐 Embedding shape:", embeddings.shape)

    print("🧱 Building FAISS index...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # inner product = cosine similarity (normalized vecs)
    index.add(embeddings)

    print("💾 Saving index & metadata...")
    faiss.write_index(index, INDEX_PATH)

    # Save metadata WITHOUT the semantic_text column (it has the "passage: " prefix,
    # not needed at query time)
    df.drop(columns=["semantic_text"]).to_csv(META_PATH, index=False)

    print("\n✅ INDEX BUILD COMPLETE")
    print("Total occupations indexed:", index.ntotal)
    print("Index file :", INDEX_PATH)
    print("Metadata   :", META_PATH)
    print("\n💡 REMINDER: In search.py, prefix every user query with 'query: '")
    print("   e.g.  model.encode('query: kisan') — NOT model.encode('kisan')")


if __name__ == "__main__":
    main()