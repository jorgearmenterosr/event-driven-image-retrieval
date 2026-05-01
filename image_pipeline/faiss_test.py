import faiss
import numpy as np

# fake image embeddings for testing
vectors = np.array([
    [0.1, 0.2, 0.3, 0.4],
    [0.9, 0.8, 0.7, 0.6],
    [0.2, 0.1, 0.4, 0.3]
]).astype("float32")

# create FAISS index
index = faiss.IndexFlatL2(4)
index.add(vectors)

# fake query embedding
query = np.array([[0.1, 0.2, 0.3, 0.4]]).astype("float32")

distances, results = index.search(query, 1)

print("Closest image index:", results[0][0])
print("Distance:", distances[0][0])