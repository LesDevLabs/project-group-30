import json
from pathlib import Path

class NotesAssistant:
    def __init__(self, data_dir="notes_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.notes_file = self.data_dir / "notes.json"
        self.notes = self.load_notes()

    # --- Завантаження та збереження ---
    def load_notes(self):
        if self.notes_file.exists():
            with open(self.notes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Note(**n) for n in data]
        return []

    def save_notes(self):
        with open(self.notes_file, "w", encoding="utf-8") as f:
            json.dump([n.to_dict() for n in self.notes], f, ensure_ascii=False, indent=4)

    # --- Основні функції ---
    def add_note(self):
        text = input("Введіть текст нотатки: ").strip()
        tags_str = input("Введіть теги через кому (опціонально): ").strip()
        tags = [t.strip() for t in tags_str.split(",")] if tags_str else []
        note = Note(text, tags)
        self.notes.append(note)
        self.save_notes()
        print("✅ Нотатку додано!")

    def edit_note(self):
        keyword = input("Введіть частину тексту нотатки для редагування: ").strip()
        results = [n for n in self.notes if keyword.lower() in n.text.lower()]
        if not results:
            print("❌ Нотатку не знайдено.")
            return
        note = results[0]
        print(f"Поточний текст: {note.text}")
        new_text = input("Новий текст (залиште порожнім, якщо не змінювати): ").strip() or note.text
        new_tags = input("Нові теги через кому (залиште порожнім, якщо не змінювати): ").strip()
        if new_tags:
            note.tags = [t.strip() for t in new_tags.split(",")]
        note.text = new_text
        self.save_notes()
        print("✏️ Нотатку оновлено!")

    def delete_note(self):
        keyword = input("Введіть частину тексту нотатки для видалення: ").strip()
        matches = [n for n in self.notes if keyword.lower() in n.text.lower()]
        if not matches:
            print("❌ Нотатку не знайдено.")
            return
        print(f"Видалено: {matches[0].text}")
        self.notes.remove(matches[0])
        self.save_notes()

    def search_notes(self):
        keyword = input("Пошук за текстом (можна залишити порожнім): ").strip()
        tag = input("Пошук за тегом (можна залишити порожнім): ").strip()
        results = self.notes
        if keyword:
            results = [n for n in results if keyword.lower() in n.text.lower()]
        if tag:
            results = [n for n in results if tag.lower() in [t.lower() for t in n.tags]]

        if not results:
            print("❌ Нотатки не знайдено.")
            return
        print("🔍 Знайдено нотатки:")
        for n in results:
            print(f"- {n.text}  [теги: {', '.join(n.tags) or 'немає'}]")

    # --- CLI ---
    def run_cli(self):
        print("=== 🗒️ Менеджер нотаток ===")
        print("Команди: add, edit, delete, search, list, exit")
        while True:
            cmd = input("\n> ").strip().lower()
            if cmd == "exit":
                print("👋 Вихід з програми...")
                break
            elif cmd == "add":
                self.add_note()
            elif cmd == "edit":
                self.edit_note()
            elif cmd == "delete":
                self.delete_note()
            elif cmd == "search":
                self.search_notes()
            elif cmd == "list":
                if not self.notes:
                    print("Поки немає нотаток.")
                else:
                    print("📘 Усі нотатки:")
                    for n in self.notes:
                        print(f"- {n.text} [теги: {', '.join(n.tags) or 'немає'}]")
            else:
                print("❓ Невідома команда. Спробуйте add / edit / delete / search / list / exit")


# --- Запуск ---
if __name__ == "__main__":
    NotesAssistant().run_cli()
