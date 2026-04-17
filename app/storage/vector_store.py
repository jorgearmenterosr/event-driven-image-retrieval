import math


class VectorStore:
    def __init__(self):
        self.vectors = {}

    def add_vector(self, image_id: str, embedding: list[float]) -> None:
        self.vectors[image_id] = embedding

    def exists(self, image_id: str) -> bool:
        return image_id in self.vectors

    def count(self) -> int:
        return len(self.vectors)

    def search(self, query_vector: list[float], top_k: int = 3) -> list[dict]:
        results = []

        for image_id, embedding in self.vectors.items():
            score = self.cosine_similarity(query_vector, embedding)
            results.append({
                "image_id": image_id,
                "score": round(score, 6),
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    @staticmethod
    def cosine_similarity(a: list[float], b: list[float]) -> float:
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)