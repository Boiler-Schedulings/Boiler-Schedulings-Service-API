import json
import numpy as np

# This script generates the embeddings

# import chromadb
from sentence_transformers import SentenceTransformer

documents = []
data_dir = "data/course_docs.json"
output_dir = "data/course_docs_emb.json"
with open(data_dir) as json_file:
   documents = json.load(json_file)

chunks = [doc["chunk"] for doc in documents]
print(chunks[0])
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(chunks)
np.save('data/embeddings.npy', embeddings)
# print(embeddings)
documents_with_embeddings = []
for i in range(len(chunks)):
   doc = documents[i]
   doc["embeddings"] = embeddings[i].tolist()
   documents_with_embeddings.append(doc)

with open(output_dir, 'w') as file:
    json.dump(documents_with_embeddings, file, indent=2)