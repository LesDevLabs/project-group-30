
class NoteRepository:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        print(" >>> add note")
        self.notes.append(note)

        print(self.notes)

    def list_note(self):
        if not self.notes:
            print("No notes yet.")
            return

        print("📘 All notes:")
        for i, n in enumerate(self.notes, start=1):
            tags = ", ".join(n.tags) if n.tags else "none"
            print(f"{i}. {n.text}  [tags: {tags}]")
