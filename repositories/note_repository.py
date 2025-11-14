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

        return f"Note {note.text} added"

    def del_note(self, note):
        if note not in self.notes:
            return "Note not found."

        deleted_text = note.text

        self.notes.remove(note)
        self.save_notes()

        return f"Note: {deleted_text} deleted"

    def find_note(self, query):
        query = query.lower().strip()

        # Find first note matching query in text or tags
        for note in self.notes:
            if query in note.text.lower() or any(query in tag.lower() for tag in note.tags):
                return note

        return None

    def search_notes(self, query=""):
        if not query:
            return self.notes

        query = query.lower().strip()
        results = [
            note for note in self.notes
            if query in note.text.lower() or any(query in tag.lower() for tag in note.tags)
        ]

        return results

    def format_notes(self, notes):
        if not notes:
            return "No notes to show."

        lines = ["📘 Notes:"]
        for i, n in enumerate(notes, start=1):
            tags = ", ".join(n.tags) if n.tags else "none"
            lines.append(f"{i}. {n.text}")
            # lines.append(f"{i}. {n.text}  [tags: {tags}]")

        return "\n".join(lines)


    def edit_note(self, note, new_text=None, new_tags=None):
        if note not in self.notes:
            return "Note not found."

        if new_text is not None:
            note.text = new_text

        if new_tags is not None:
            note.tags = new_tags

        self.save_notes()

        return f"Note {note.text} updated"
        # return f"Note updated: {note.text} [tags: {', '.join(note.tags) if note.tags else 'none'}]"
