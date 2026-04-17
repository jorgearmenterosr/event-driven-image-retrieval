class DocumentStore:
    def __init__(self):
        self.documents = {}

    def insert_document(self, document: dict) -> None:
        image_id = document["image_id"]
        self.documents[image_id] = document

    def get_document(self, image_id: str):
        return self.documents.get(image_id)

    def exists(self, image_id: str) -> bool:
        return image_id in self.documents

    def count(self) -> int:
        return len(self.documents)