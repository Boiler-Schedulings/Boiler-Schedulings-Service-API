import chromadb
import numpy as np
import json

def process_data_and_query(data_dir, query_texts, n_results):
    chroma_client = chromadb.Client()

    collection = chroma_client.create_collection(name="course_catalog")

    # Load data from JSON file
    with open(data_dir) as json_file:
        documents = json.load(json_file)

    embeddings = [doc["embeddings"] for doc in documents]
    docs = [doc["chunk"] for doc in documents]
    ids = [str(i) for i in range(len(embeddings))]

    # Halved because the maximum batch size is 5461 :(
    half = int(len(embeddings) / 2)
    collection.add(
        embeddings=embeddings[:half],
        documents=docs[:half],
        ids=ids[:half]
    )

    collection.add(
        embeddings=embeddings[half:],
        documents=docs[half:],
        ids=ids[half:]
    )

    results = collection.query(
        query_texts=query_texts,
        n_results=n_results
    )

    courses = []
    for document in results['documents'][0]:
        courses.append(document)

    return courses

# Example usage:
# data_dir = "data/course_docs_emb.json"
# query_texts = ["I want a course about the applications of corn that is 1 credit."]
# n_results = 4

# process_data_and_query(data_dir, query_texts, n_results)
