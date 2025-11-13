from cli.command_suggester import CommandSuggester
from repositories.contact_repository import ContactRepository
from handlers.command_handler import CommandHandler
from cli.presenter import Presenter
from utils.utils import parse_user_input_data


def main():
    # Initialize repositories and handlers
    # TODO load data
    repository = ContactRepository()
    command_handler = CommandHandler(repository)
    command_suggester = CommandSuggester()

    # Display welcome message
    Presenter.print_welcome()

    # Main loop
    while True:
        try:
            # Get user input with colored prompt
            user_input = input(Presenter.print_prompt())
            command, *args = parse_user_input_data(user_input)
            if command in ['close', 'exit', 'quit']:
                print("Good bye!")
                #TODO save_data()
                break
            if (command_handler[command]):
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


if __name__ == "__main__":
    main()
