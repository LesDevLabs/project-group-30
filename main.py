from repositories.contact_repository import ContactRepository
from handlers.command_handler import CommandHandler
from cli.command_router import CommandRouter
from cli.presenter import Presenter


def main():
    """Main entry point for Personal Assistant CLI"""
    # Initialize repositories and handlers
    repository = ContactRepository()
    command_handler = CommandHandler(repository)

    # Initialize CLI components
    router = CommandRouter(command_handler)

    # Display welcome message
    Presenter.print_welcome()

    # Main loop
    while True:
        try:
            # Get user input with colored prompt
            user_input = input(Presenter.print_prompt())

            # Route command
            should_continue, result = router.route(user_input)

            # Display result if any
            if result:
                # Handle special formatting for contact lists
                if "Found" in result and "contacts:" in result:
                    # Multiple contacts found from search
                    lines = result.split('\n')
                    print(Presenter.info(lines[0]))  # "Found X contacts:"
                    for contact_line in lines[1:]:
                        if contact_line.strip():  # Skip empty lines
                            Presenter.print_contact(contact_line)
                elif ("No contacts stored" in result or
                      "No contacts found" in result):
                    print(Presenter.info(result))
                elif "Contact name:" in result:
                    # Single contact display
                    Presenter.print_contact(result)
                elif result.count('\n') > 0 and "Contact name:" in result:
                    # Multiple contacts (from 'all' command)
                    contacts = result.split('\n')
                    for contact in contacts:
                        if contact.strip():  # Skip empty lines
                            Presenter.print_contact(contact)
                else:
                    # Regular message (already formatted by router)
                    print(result)

            # Check if should exit
            if not should_continue:
                break

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