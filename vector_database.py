import chromadb
import numpy as np
import json
from sentence_transformers import SentenceTransformer

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="course_catalog")

data_dir = "data/course_docs_emb.json"
with open(data_dir) as json_file:
    documents = json.load(json_file)

embeddings = [doc["embeddings"] for doc in documents]
docs = [doc["chunk"] for doc in documents]
ids = [str(i) for i in range(len(embeddings))]

collection.add(
    embeddings=embeddings,
    documents=docs,
    ids=ids
)

def query_course_catalog(query_texts, n_results=2):
    results = collection.query(
        query_texts=query_texts,
        n_results=n_results
    )
    return [course for course in results['documents'][0]]

print(query_course_catalog("I want to take a class about Mars"))




# reddit_collection = chroma_client.create_collection(name="reddit_documents")

# with open("data/reddit_docs.jsonl", "r") as jsonl_file:
#     reddit_docs = [json.loads(line) for line in jsonl_file]

# reddit_embeddings = np.load("data/reddit_embeddings.npy")
# print(reddit_embeddings[:5])
# reddit_ids = [f"id{i}" for i in range(len(reddit_docs))]
# docs = [doc['chunk'] for doc in reddit_docs]
# reddit_collection.add(
#     embeddings=reddit_embeddings,
#     documents=docs,
#     ids=reddit_ids
# )

# def query_reddit(query_texts, n_results=2):
#     results = reddit_collection.query(
#         query_texts=query_texts,
#         n_results=n_results
#     )
#     return results['documents'][0]

# print(query_reddit("Who is a bad teacher for CS 182?"))

