from cli.presenter import Presenter
from models.contact import Record
from handlers.decorators import input_error

class CommandHandler:
    def __init__(self, repository):
        self.repository = repository
        self.commands = {
            "add": self.add_contact,
            "show": self.show_contact,
            "all": self.show_all_contacts,
            "change": self.change,
            "rename": self.edit_name,
            "delete": self.delete_contact,
            "delete-phone": self.delete_phone,
            "search-contact" : self.search_contacts,
            "help": self._handle_help
        }

    def __getitem__(self, key):
        return self.commands.get(key)

    @input_error
    def add_contact(self):
        print("Let's create a new contact. Name is required. Other fields are optional")
        print("Press Enter to skip any optional field.\n")
        while True:
            name = input("Name(required): ").strip()
            if not name:
                print("Name is required. Please enter a name.\n")
                continue
            break

        contact = self.repository.find_contact(name)
        
        if contact is None:
            contact = Record(name)
            self.repository.add_contact(contact)
        else:
            return "Contact alreade exist, please use update to modify"

        
        phone = input("Phone (optional): ").strip() or None
        if phone:
            contact.add_phone(phone)
        
        email = input("Email (optional): ").strip() or None
        if email:
            contact.add_email(email)
        
        address = input("Address (optional): ").strip() or None
        if address:
            contact.set_address(address)
        
        birthday = input("Birthday (optional, dd.mm.yyyy): ").strip() or None
        if birthday:
            contact.set_birthday(birthday)

        return "Contact added."

    @input_error
    def show_contact(self, name: str):
        """Show a specific contact"""
        contact = self.repository.find_contact(name)
        if contact is None:
            raise KeyError(f"Contact {name} not found.")
        return str(contact)

    @input_error
    def show_all_contacts(self):
        """Show all contacts"""
        contacts = self.repository.get_all_contacts()
        if not contacts:
            return "No contacts stored."
        return "\n".join(str(contact) for contact in contacts)

    @input_error
    def change(self, name: str, old_phone: str, new_phone: str) -> str:
        """Change a phone number for a contact"""
        record = self.repository.find_contact(name)
        if record is None:
            raise KeyError(f"Contact {name} not found.")
        record.edit_phone(old_phone, new_phone)
        return f"Phone number for {name} changed from {old_phone} to {new_phone}."

    @input_error
    def edit_name(self, old_name: str, new_name: str) -> str:
        """Rename a contact"""
        record = self.repository.find_contact(old_name)
        if not record:
            raise KeyError(f"Contact {old_name} not found.")

        if self.repository.find_contact(new_name):
            raise ValueError(f"Contact {new_name} already exists.")

        self.repository.delete_contact(old_name)
        record.name.value = new_name
        self.repository.add_contact(record)

        return f"Contact name changed from {old_name} to {new_name}."

    @input_error
    def delete_contact(self, name: str):
        """Delete a contact"""
        record = self.repository.find_contact(name)
        if record is None:
            raise KeyError(f"Contact {name} not found.")
        self.repository.delete_contact(name)
        return f"Contact {name} deleted successfully."

    @input_error
    def delete_phone(self, name: str, phone: str) -> str:
        """Delete a phone number from a contact"""
        record = self.repository.find_contact(name)
        if not record:
            raise KeyError(f"Contact {name} not found.")

        phone_obj = record.find_phone(phone)
        if not phone_obj:
            raise ValueError(f"Phone {phone} not found for contact {name}.")

        record.remove_phone(phone)
        return f"Phone {phone} removed from contact {name}."

    @input_error
    def search_contacts(self, query: str) -> str:
        exact_results = self.repository.search_contacts(query)

        if exact_results:
            if len(exact_results) == 1:
                return str(exact_results[0])

            lines = [f"Found {len(exact_results)} contacts:"]
            lines.extend(str(contact) for contact in exact_results)
            return "\n".join(lines)

        closest = self.repository.search_closest_contacts(query)

        if closest:
            lines = [
                f"No exact matches for '{query}':",
                "Most similar contacts:"
             ]
            lines.extend(str(contact) for contact in closest)
            return "\n".join(lines)

        return f"No contacts found matching '{query}'."
    

    def _handle_help(self):
        header = Presenter.header("Available Commands:")

        add_cmd = (
            f"  {Presenter.info('add <name> [phone] [email] [address] [birthday]')}\n"
            f"    Add or update a contact\n"
        )

        show_cmd = (
            f"  {Presenter.info('show <name>')}\n"
            f"    Show a specific contact\n"
        )

        all_cmd = (
            f"  {Presenter.info('all')}\n"
            f"    Show all contacts\n"
        )

        search_cmd = (
            f"  {Presenter.info('search-contacts <query>')}\n"
            f"    Search contacts by name, phone, or email\n"
        )

        change_cmd = (
            f"  {Presenter.info('change <name> <old-phone> <new-phone>')}\n"
            f"    Change a phone number\n"
        )

        rename_cmd = (
            f"  {Presenter.info('rename <old-name> <new-name>')}\n"
            f"    Rename a contact\n"
        )

        delete_cmd = (
            f"  {Presenter.info('delete <name>')}\n"
            f"    Delete a contact\n"
        )

        delete_phone_cmd = (
            f"  {Presenter.info('delete-phone <name> <phone>')}\n"
            f"    Delete a phone number from a contact\n"
        )

        system_header = f"{Presenter.highlight('System:')}\n"

        help_cmd = (
            f"  {Presenter.info('help [command]')}\n"
            f"    Show this help message\n"
        )

        exit_cmd = (
            f"  {Presenter.info('exit / quit / close')}\n"
            f"    Exit the application\n"
        )

        example = (
            f"{Presenter.warning('Example:')} "
            f"add John 1234567890 john@example.com '123 Main St' 01.01.1990\n"
        )

        help_text = (
            header
            + add_cmd
            + show_cmd
            + all_cmd
            + search_cmd
            + change_cmd
            + rename_cmd
            + delete_cmd
            + delete_phone_cmd
            + system_header
            + help_cmd
            + exit_cmd
            + example
        )

        return help_text
