import chromadb
import numpy as np
import json
from sentence_transformers import SentenceTransformer

chroma_client = chromadb.Client()

reddit_collection = chroma_client.create_collection(name="reddit_posts")
with open("data/reddit_docs.jsonl", "r") as jsonl_file:
    reddit_docs = [json.loads(line) for line in jsonl_file]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
chunks = [x['chunk'] for x in reddit_docs]
embeddings = model.encode(chunks)
np.save('data/reddit_embeddings.npy', embeddings)
