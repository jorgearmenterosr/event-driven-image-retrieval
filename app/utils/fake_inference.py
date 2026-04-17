def run_fake_inference(image_id: str):
    return [
        {
            "label": "car",
            "bbox": [12, 44, 188, 200],
            "conf": 0.93,
        },
        {
            "label": "person",
            "bbox": [230, 51, 286, 210],
            "conf": 0.88,
        },
    ]