# build_index.py (UPGRADED - MULTILINGUAL)

import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/skillweave_clean.csv"
INDEX_PATH = "skillweave.index"
META_PATH = "skillweave_metadata.csv"

MODEL_NAME = "intfloat/multilingual-e5-base"
BATCH_SIZE = 64
TOP_TEXT_LEN = 1200


def build_semantic_text(row):
    parts = [
        f"Job Title: {row['title']}",
        f"Description: {row['description']}",
        f"Division: {row['division_name']}",
        f"Sub Division: {row['sub_division_name']}",
        f"Group: {row['group_name']}",
        f"Family: {row['family_name']}",
    ]

    text = ". ".join([p for p in parts if isinstance(p, str)])
    
    # 🔥 E5 requires "passage:" prefix
    return "passage: " + text[:TOP_TEXT_LEN]


def main():
    print("📄 Loading dataset...")
    df = pd.read_csv(DATA_PATH, dtype=str, keep_default_na=False)

    print("🧠 Building semantic text...")
    df["semantic_text"] = df.apply(build_semantic_text, axis=1)

    texts = df["semantic_text"].tolist()

    print("🤖 Loading multilingual model...")
    model = SentenceTransformer(MODEL_NAME)

    print("⚙️ Creating embeddings...")
    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    print("💾 Saving index...")
    faiss.write_index(index, INDEX_PATH)
    df.drop(columns=["semantic_text"]).to_csv(META_PATH, index=False)

    print("✅ Multilingual Index Built Successfully!")


if __name__ == "__main__":
    main()