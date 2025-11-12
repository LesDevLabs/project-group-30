import shlex
from repositories.contact_repository import ContactRepository
from handlers.command_handler import CommandHandler


def parse_command(user_input: str):
    """Parse user input into command and arguments, handling quoted strings"""
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


def main():
    repository = ContactRepository()
    contact_service = CommandHandler(repository)

    print("Welcome to the Contact Book!")
    print("Commands: add, show, all, change, rename, "
          "delete, delete-phone, exit")
    example = ("Example: add John 1234567890 "
               "john@example.com '123 Main St' 01.01.1990")
    print(example)

    while True:
        user_input = input("\nEnter a command: ")
        command, args = parse_command(user_input)

        if command in ["exit", "close", "quit"]:
            print("Goodbye!")
            break
        elif command == "add":
            if len(args) < 1:
                print("Error: Please provide at least a name.")
                continue
            name = args[0]
            phone = args[1] if len(args) > 1 else None
            email = args[2] if len(args) > 2 else None
            address = args[3] if len(args) > 3 else None
            birthday = args[4] if len(args) > 4 else None
            print(contact_service.add_contact(name, phone, email,
                                              address, birthday))
        elif command == "show":
            if len(args) < 1:
                print("Error: Please provide a contact name.")
                continue
            print(contact_service.show_contact(args[0]))
        elif command == "all":
            print(contact_service.show_all_contacts())
        elif command == "change":
            if len(args) < 3:
                print("Error: Please provide contact name, "
                      "old phone, and new phone.")
                continue
            print(contact_service.change(args[0], args[1], args[2]))
        elif command == "rename":
            if len(args) < 2:
                print("Error: Please provide old name and new name.")
                continue
            print(contact_service.edit_name(args[0], args[1]))
        elif command == "delete":
            if len(args) < 1:
                print("Error: Please provide a contact name.")
                continue
            print(contact_service.delete_contact(args[0]))
        elif command == "delete-phone":
            if len(args) < 2:
                print("Error: Please provide contact name and phone number.")
                continue
            print(contact_service.delete_phone(args[0], args[1]))
        else:
            print("Invalid command. Use: add, show, all, change, "
                  "rename, delete, delete-phone, exit")


if __name__ == "__main__":
    main()
