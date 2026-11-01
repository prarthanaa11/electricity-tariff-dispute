import hashlib
import json
import time

from pathlib import Path

import fitz

from langchain_text_splitters import RecursiveCharacterTextSplitter


RAW_DIR = Path("corpus/raw")
PROCESSED_DIR = Path("corpus/processed")
INDEX_DIR = Path("data/index")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
INDEX_DIR.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for block in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def extract_pages(pdf_path: Path) -> list[dict]:
    pages = []

    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(
            document,
            start=1,
        ):
            text = page.get_text("text").strip()

            if text:
                pages.append(
                    {
                        "document_id": pdf_path.stem,
                        "document_name": pdf_path.name,
                        "page": page_number,
                        "text": text,
                        "sha256": sha256_file(pdf_path),
                    }
                )

    return pages


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 900,
    chunk_overlap: int = 150,
) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = []

    for page in pages:
        pieces = splitter.split_text(page["text"])

        for index, piece in enumerate(pieces):
            chunks.append(
                {
                    "chunk_id": (
                        f'{page["document_id"]}:'
                        f'{page["page"]}:{index}'
                    ),
                    "document_id": page["document_id"],
                    "document_name": page["document_name"],
                    "page": page["page"],
                    "text": piece,
                    "sha256": page["sha256"],
                }
            )

    return chunks


def run_ingestion():
    start = time.perf_counter()

    pdf_files = sorted(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        raise RuntimeError(
            "No PDFs found in corpus/raw. "
            "Download the official documents first."
        )

    all_pages = []

    for pdf_path in pdf_files:
        print(f"Extracting: {pdf_path.name}")

        pages = extract_pages(pdf_path)

        if not pages:
            print(
                f"WARNING: No selectable text found "
                f"in {pdf_path.name}. OCR may be required."
            )

        all_pages.extend(pages)

    if not all_pages:
        raise RuntimeError(
            "No text extracted from any PDF."
        )

    chunks = chunk_pages(all_pages)

    output_path = PROCESSED_DIR / "chunks.jsonl"

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        for chunk in chunks:
            file.write(
                json.dumps(chunk, ensure_ascii=False)
                + "\n"
            )

    elapsed = time.perf_counter() - start

    manifest = {
        "documents": [
            {
                "name": path.name,
                "sha256": sha256_file(path),
            }
            for path in pdf_files
        ],
        "page_count": len(all_pages),
        "chunk_count": len(chunks),
        "elapsed_seconds": round(elapsed, 3),
        "chunks_per_second": round(
            len(chunks) / max(elapsed, 0.001),
            3,
        ),
    }

    (
        INDEX_DIR / "ingestion_manifest.json"
    ).write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    run_ingestion()