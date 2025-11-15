from models.contact import Record
from models.note import Note

from search.search_service import SearchService


class ContactRepository:
    def __init__(self):
        self.contacts = {}
        self.search_service = SearchService()
        self.notes = []

    def add_contact(self, record: Record):
        """Add a new contact or update existing one"""
        self.contacts[record.name.value] = record

    def find_contact(self, name: str) -> Record:
        """Find a contact by name"""
        return self.contacts.get(name)

    def delete_contact(self, name: str):
        """Delete a contact by name"""
        if name in self.contacts:
            del self.contacts[name]
            return True
        return False

    def get_all_contacts(self):
        """Get all contacts"""
        return list(self.contacts.values())

    def has_contact(self, name: str) -> bool:
        """Check if contact exists"""
        return name in self.contacts

    def search_contacts(self, query: str):
        return self.search_service.exact_search(self.contacts, query)

    def search_closest_contacts(self, query: str):
        return self.search_service.fuzzy_search(self.contacts, query)

    # --- Notes ---
    def add_note(self, note):
        self.notes.append(note)
        return self.format_notes(note, " Note added:")

    def del_note(self, note):
        if note not in self.notes:
            return "Note not found."

        deleted_text = note.text

        self.notes.remove(note)

        return f"Note: {deleted_text} deleted"

    def find_note(self, query):
        query = query.lower().strip()

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

    def format_notes(self, notes, header=""):
        if notes is None or (isinstance(notes, list) and not notes):
            return "No notes to show."

        if isinstance(notes, Note):
            notes = [notes]

        lines = []

        if header:
            lines.append(header)

        if len(notes) == 1:
            lines.append(str(notes[0]))
        else:
            for i, note in enumerate(notes, start=1):
                lines.append(f"{i}. {str(note)}")

        return "\n".join(lines)

    def edit_note(self, note, new_text=None, new_tags=None):
        if note not in self.notes:
            return "Note not found."

        if new_text is not None:
            note.text = new_text

        if new_tags is not None:
            note.tags = new_tags

        return f"Note {note.text} updated"
