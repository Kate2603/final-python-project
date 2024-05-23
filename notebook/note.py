class Note:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.tags = tags or []

    def __str__(self):
        return f"{self.title}: {self.content} Tags: {', '.join(self.tags)}"