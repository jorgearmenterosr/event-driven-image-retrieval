import hashlib
import random


def create_fake_embedding(image_id: str, dimension: int = 8) -> list[float]:
    seed_value = int(hashlib.md5(image_id.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed_value)
    return [round(rng.random(), 6) for _ in range(dimension)]