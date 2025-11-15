
class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []

    def to_dict(self):
        return {"text": self.text, "tags": self.tags}
