# build_index.py
# SkillWeave – Semantic Index Builder (SentenceTransformer)

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

MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
BATCH_SIZE = 64          # safe for CPU
TOP_TEXT_LEN = 1200      # avoid extremely long rows
# ---------------------------------------


def build_semantic_text(row):
    """
    Create a rich semantic representation for each occupation.
    This is CRITICAL for good results.
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
    return text[:TOP_TEXT_LEN]


def main():
    print("📄 Loading dataset...")
    df = pd.read_csv(DATA_PATH, dtype=str, keep_default_na=False)
    print(f"✅ Rows loaded: {len(df)}")

    print("🧠 Building semantic text...")
    df["semantic_text"] = df.apply(build_semantic_text, axis=1)

    texts = df["semantic_text"].tolist()

    print("🤖 Loading SentenceTransformer model...")
    model = SentenceTransformer(MODEL_NAME)

    print("⚙️ Creating embeddings (batched)...")
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
    index = faiss.IndexFlatIP(dim)  # cosine similarity
    index.add(embeddings)

    print("💾 Saving index & metadata...")
    faiss.write_index(index, INDEX_PATH)

    df.drop(columns=["semantic_text"]).to_csv(META_PATH, index=False)

    print("\n✅ INDEX BUILD COMPLETE")
    print("Total occupations indexed:", index.ntotal)
    print("Index file :", INDEX_PATH)
    print("Metadata   :", META_PATH)


if __name__ == "__main__":
    main()
