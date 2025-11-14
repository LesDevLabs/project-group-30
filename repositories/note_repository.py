import json
from pathlib import Path
from models.note import Note

class NoteRepository:
    def __init__(self, data_dir="notes_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.notes_file = self.data_dir / "notes.json"
        self.notes = self.load_notes()

    # --- Load & Save ---
    def load_notes(self):
        if self.notes_file.exists():
            with open(self.notes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Note(**n) for n in data]
        return []

    def save_notes(self):
        with open(self.notes_file, "w", encoding="utf-8") as f:
            json.dump([n.to_dict() for n in self.notes], f, ensure_ascii=False, indent=4)

    # --- Functional ---
    def add_note(self, note):
        self.notes.append(note)
        self.save_notes()
        
    def list_note(self):
        if not self.notes:
            print("No notes yet.")
            return

        print("📘 All notes:")
        for i, n in enumerate(self.notes, start=1):
            tags = ", ".join(n.tags) if n.tags else "none"
            print(f"{i}. {n.text}  [tags: {tags}]")
