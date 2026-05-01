import redis
from PIL import Image

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

pubsub = r.pubsub()
pubsub.subscribe("image_channel")

print("Waiting for images...")

for message in pubsub.listen():
    if message["type"] == "message":
        image_path = message["data"]
        
        try:
            img = Image.open(image_path)
            print(f"Processed {image_path}")
            print("Size:", img.size)
            print("Mode:", img.mode)
        except Exception as e:
            print("Error:", e)