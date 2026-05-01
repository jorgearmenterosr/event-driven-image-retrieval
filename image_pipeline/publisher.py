import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

image_path = "image1.png"

r.publish("image_channel", image_path)

print("Image sent to processing")