
class Note:
    def __init__(self, text, tags=None):
        self.text = text

        if tags is None:
            self.tags = []
        elif isinstance(tags, str):
            self.tags = [tags]
        else:
            self.tags = list(tags)

        # Optionally — convert tags to lowercase
        # self.tags = [t.lower() for t in self.tags]

    def to_dict(self):
        return {"text": self.text, "tags": self.tags}

    def __str__(self):
        if self.tags:
            tags_str = ", ".join(self.tags)
            return f'📝 {self.text}  [Tags: {tags_str}]'
        else:
            return f'📝 {self.text}'