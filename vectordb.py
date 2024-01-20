import chromadb
import numpy as np
import json

data_dir = "data/course_docs_emb.json"
chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="course_catalog")

documents = []

with open(data_dir) as json_file:
   documents = json.load(json_file)

embeddings = [doc["embeddings"] for doc in documents]
docs = [doc["chunk"] for doc in documents]
ids = [f"id{i}" for i in range(len(embeddings))]

collection.add(
    embeddings=embeddings,
    documents=docs,
    ids=ids
)

results = collection.query(
    query_texts=["I want a course about the applications of corn that is 1 credit."],
    n_results=4
)
print("Total Documents", len(embeddings))
for document in results['documents'][0]:
   print(document, "\n")