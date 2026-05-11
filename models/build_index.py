import json
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"
INDEX_FILE = "shl_index.faiss"
CATALOG_FILE = "catalog.json"


def load_catalog():
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_embeddings(model, texts):
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    return index


def save_index(index):
    faiss.write_index(index, INDEX_FILE)


def main():

    print("Loading catalog...")
    catalog = load_catalog()
    texts = [item["search_text"] for item in catalog]
    print(f"Loaded {len(texts)} documents")
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    print("Generating embeddings...")
    embeddings = build_embeddings(model, texts)
    print("Building FAISS index...")
    index = build_faiss_index(embeddings)
    print("Saving index...")
    save_index(index)
    print("Index saved successfully")

if __name__ == "__main__":
    main()