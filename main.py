"""
Main entry point for the Contact & Task Assistant Bot.
Handles the main loop, command parsing, and routing.
"""

import shlex

from handlers.command_handler import CommandHandler
from repositories.contact_repository import ContactRepository
from repositories.task_repository import TaskRepository


def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Parse user input into command and arguments."""
    parts = user_input.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


def parse_command(user_input: str):
    """Parse user input into command and arguments, handling quoted strings (legacy)"""
    try:
        parts = shlex.split(user_input.strip())
    except ValueError:
        # Fallback to simple split if shlex fails
        parts = user_input.strip().split()

    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def show_welcome():
    """Display welcome message."""
    print("=" * 50)
    print("Welcome to the Contact & Task Assistant Bot!")
    print("=" * 50)
    print('Type "help" for available commands.')
    print()


def show_help():
    """Display help message with all available commands."""
    help_text = """
Available commands:

  hello                 - Start the bot
  help                  - Show this help message
  
  add                   - Add contact or task (interactive menu)
  add contact           - Add new contact directly
  add task              - Add new task directly
  
  find                  - Find contact or task (interactive menu)
  
  change                - Change contact or task (interactive menu)
  change phone          - Change phone number
  change name           - Change contact name
  change email          - Change email
  change address        - Change address
  change birthday       - Change birthday
  change task           - Change task
  change tags           - Change task tags
  
  delete                - Delete contact or task
  
  all                   - Show all contacts or tasks
  
  sort                  - Sort contacts or tasks
  
  close / exit          - Exit the bot
"""
    print(help_text)


def main():
    """Main bot loop with full command processing."""
    contact_repository = ContactRepository()
    task_repository = TaskRepository()
    command_handler = CommandHandler(contact_repository, task_repository)

    show_welcome()
    started = False

    while True:
        try:
            user_input = input(">>> ").strip()

            if not user_input:
                continue

            command, args = parse_input(user_input)

            # Initial greeting required
            if not started:
                if command == "hello":
                    started = True
                    print(
                        "\nHow can I help you? You can add, change, or view contacts."
                    )
                    print('Type "help" for assistance.\n')
                else:
                    print('Please say "hello" to start.\n')
                continue

            # Exit commands
            if command in ["close", "exit", "goodbye", "quit"]:
                print("\nGood bye! Have a great day!")
                break

            # Help command
            if command == "help":
                show_help()
                continue

            # Main command routing
            result = None

            # ADD command
            if command == "add":
                if args and args[0] == "contact":
                    result = command_handler.contact_handler.add_contact_interactive()
                elif args and args[0] == "task":
                    result = command_handler.task_handler.add_task_interactive()
                else:
                    # Interactive menu
                    result = command_handler.route_add_command(args)

            # FIND command
            elif command == "find":
                result = command_handler.route_find_command(args)

            # CHANGE command
            elif command == "change":
                result = command_handler.route_change_command(args)

            # DELETE command
            elif command == "delete":
                result = command_handler.route_delete_command(args)

            # ALL command
            elif command == "all":
                result = command_handler.route_all_command(args)

            # SORT command
            elif command == "sort":
                result = command_handler.route_sort_command(args)

            # Legacy commands for backward compatibility
            elif command == "add":
                if len(args) < 1:
                    print("Error: Please provide at least a name.")
                    continue

                name = args[0]
                phone = args[1] if len(args) > 1 else None
                email = args[2] if len(args) > 2 else None
                address = args[3] if len(args) > 3 else None
                birthday = args[4] if len(args) > 4 else None
                result = command_handler.add_contact(
                    name, phone, email, address, birthday
                )

            elif command == "show":
                if len(args) < 1:
                    print("Error: Please provide a contact name.")
                    continue
                result = command_handler.show_contact(args[0])

            elif command == "rename":
                if len(args) < 2:
                    print("Error: Please provide old name and new name.")
                    continue
                result = command_handler.edit_name(args[0], args[1])

            elif command == "delete-phone":
                if len(args) < 2:
                    print("Error: Please provide contact name and phone number.")
                    continue
                result = command_handler.delete_phone(args[0], args[1])

            else:
                result = (
                    f'Unknown command: "{command}". Type "help" for available commands.'
                )

            if result:
                print(f"\n{result}\n")

        except KeyboardInterrupt:
            print("\n\nGood bye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
