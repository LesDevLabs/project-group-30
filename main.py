import sys

from cli.command_suggester import CommandSuggester
from cli.presenter import Presenter
from handlers.command_handler import CommandHandler
from repositories.contact_repository import ContactRepository
from repositories.note_repository import NoteRepository
from storage.factory import StorageFactory
from utils.utils import parse_user_input_data


def main():
    # Initialize repositories and handlers
    storage_type = sys.argv[1] if len(sys.argv) > 1 else "pkl"

    try:
        storage = StorageFactory.create_storage(storage_type)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    repository = storage.load()
    if not isinstance(repository, ContactRepository):
        repository = ContactRepository()

    note_repo = NoteRepository()
    command_handler = CommandHandler(repository, note_repo)
    command_suggester = CommandSuggester()

    # Display welcome message
    Presenter.print_welcome()

    # Main loop
    try:
        while True:
            try:
                # Get user input with colored prompt
                user_input = input(Presenter.print_prompt())
                command, *args = parse_user_input_data(user_input)
                if command in ["close", "exit", "quit"]:
                    print("Good bye!")
                    break
                if command_handler[command]:
                    print(command_handler[command](*args))
                else:
                    print(command_suggester.get_suggestion_message(command))

            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print("\n" + Presenter.info("Goodbye!"))
                break
            except EOFError:
                # Handle Ctrl+D gracefully
                print("\n" + Presenter.info("Goodbye!"))
                break
            except Exception as e:
                # Handle unexpected errors
                print(Presenter.error(f"Unexpected error: {str(e)}"))
    finally:
        storage.save(repository)


if __name__ == "__main__":
    main()
