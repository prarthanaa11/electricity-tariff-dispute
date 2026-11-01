import json

from pathlib import Path

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


CHUNKS_PATH = Path("corpus/processed/chunks.jsonl")
INDEX_DIR = Path("data/index")

FAISS_PATH = INDEX_DIR / "regulations.faiss"
METADATA_PATH = INDEX_DIR / "metadata.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks():
    with CHUNKS_PATH.open(
        encoding="utf-8"
    ) as file:
        return [
            json.loads(line)
            for line in file
            if line.strip()
        ]


def build_index():
    if not CHUNKS_PATH.exists():
        raise RuntimeError(
            "Run the ingestion pipeline first."
        )

    chunks = load_chunks()

    if not chunks:
        raise RuntimeError("No chunks to index.")

    model = SentenceTransformer(MODEL_NAME)

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True,
    )

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32,
    )

    index = faiss.IndexFlatIP(
        embeddings.shape[1]
    )

    index.add(embeddings)

    INDEX_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    faiss.write_index(
        index,
        str(FAISS_PATH),
    )

    METADATA_PATH.write_text(
        json.dumps(
            {
                "model": MODEL_NAME,
                "chunk_count": len(chunks),
                "chunks": chunks,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        f"Indexed {len(chunks)} regulation chunks."
    )


if __name__ == "__main__":
    build_index()