"""
Prepare TinyShakespeare dataset as an alternative to HuggingFace data.
Downloads from GitHub and converts to the parquet format expected by autoresearch.

Usage:
    python prepare_shakespeare.py
"""

import os
import requests
import pyarrow as pa
import pyarrow.parquet as pq

# Configuration
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "autoresearch")
DATA_DIR = os.path.join(CACHE_DIR, "data")
SHAKESPEARE_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"

def download_shakespeare():
    """Download TinyShakespeare from GitHub."""
    print("Downloading TinyShakespeare from GitHub...")
    response = requests.get(SHAKESPEARE_URL)
    response.raise_for_status()
    return response.text

def split_into_documents(text, chunk_size=2000):
    """Split text into document chunks (roughly paragraph-based)."""
    # Split by double newlines (scene/act breaks) first
    sections = text.split('\n\n')

    documents = []
    current_doc = ""

    for section in sections:
        if len(current_doc) + len(section) < chunk_size:
            current_doc += section + "\n\n"
        else:
            if current_doc.strip():
                documents.append(current_doc.strip())
            current_doc = section + "\n\n"

    if current_doc.strip():
        documents.append(current_doc.strip())

    return documents

def create_parquet_shards(documents, docs_per_shard=50):
    """Create parquet shards from documents."""
    os.makedirs(DATA_DIR, exist_ok=True)

    # Split into training and validation
    val_split = int(len(documents) * 0.9)
    train_docs = documents[:val_split]
    val_docs = documents[val_split:]

    print(f"Total documents: {len(documents)}")
    print(f"Training documents: {len(train_docs)}")
    print(f"Validation documents: {len(val_docs)}")

    # Create training shards
    shard_idx = 0
    for i in range(0, len(train_docs), docs_per_shard):
        chunk = train_docs[i:i + docs_per_shard]
        table = pa.table({'text': chunk})
        filepath = os.path.join(DATA_DIR, f"shard_{shard_idx:05d}.parquet")
        pq.write_table(table, filepath)
        print(f"  Created {filepath} ({len(chunk)} documents)")
        shard_idx += 1

    num_train_shards = shard_idx

    # Create validation shard (shard_06542 to match expected VAL_SHARD)
    table = pa.table({'text': val_docs})
    val_filepath = os.path.join(DATA_DIR, "shard_06542.parquet")
    pq.write_table(table, val_filepath)
    print(f"  Created {val_filepath} ({len(val_docs)} documents) [VALIDATION]")

    return num_train_shards

def main():
    print(f"Cache directory: {CACHE_DIR}")
    print()

    # Download
    text = download_shakespeare()
    print(f"Downloaded {len(text):,} characters")
    print()

    # Split into documents
    documents = split_into_documents(text)
    print(f"Split into {len(documents)} documents")
    print()

    # Create parquet files
    print("Creating parquet shards...")
    num_shards = create_parquet_shards(documents)
    print()

    print(f"Done! Created {num_shards} training shards + 1 validation shard")
    print(f"Data ready at: {DATA_DIR}")
    print()
    print("Now run: uv run prepare.py")
    print("(This will skip download and just train the tokenizer)")

if __name__ == "__main__":
    main()
