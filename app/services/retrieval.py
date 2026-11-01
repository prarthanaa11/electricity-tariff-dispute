import json

from pathlib import Path

import faiss

from sentence_transformers import SentenceTransformer


INDEX_PATH = Path("data/index/regulations.faiss")
METADATA_PATH = Path("data/index/metadata.json")


class RegulationRetriever:
    def __init__(self):
        if not INDEX_PATH.exists():
            raise RuntimeError(
                "FAISS index not found. "
                "Build the index first."
            )

        self.index = faiss.read_index(
            str(INDEX_PATH)
        )

        metadata = json.loads(
            METADATA_PATH.read_text(
                encoding="utf-8"
            )
        )

        self.chunks = metadata["chunks"]
        self.model_name = metadata["model"]

        self.model = SentenceTransformer(
            self.model_name
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        if not query.strip():
            return []

        vector = self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        scores, indices = self.index.search(
            vector.astype("float32"),
            min(top_k, len(self.chunks)),
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):
            if index < 0:
                continue

            chunk = self.chunks[int(index)]

            results.append(
                {
                    **chunk,
                    "similarity": float(score),
                }
            )

        return results
    