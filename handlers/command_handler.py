from cli.presenter import Presenter
from models.contact import Record
from handlers.decorators import input_error
from handlers.birthday_service import BirthdayService


class CommandHandler:
    def __init__(self, repository):
        self.repository = repository
        self.birthday_service = BirthdayService(repository)
        self.commands = {
            "add": self.add_contact,
            "show": self.show_contact,
            "all": self.show_all_contacts,
            "change": self.change,
            "rename": self.edit_name,
            "delete": self.delete_contact,
            "delete-phone": self.delete_phone,
            "search-contact": self.search_contacts,
            "birthdays": self.show_birthdays,
            "help": self._handle_help
        }

    def __getitem__(self, key):
        return self.commands.get(key)

    @input_error
    def add_contact(self):
        print(Presenter.info(
            "Let's create a new contact. "
            "Name is required. Other fields are optional"
        ))
        print(Presenter.info("Press Enter to skip any optional field."))
        while True:
            name = input("Name(required): ").strip()
            if not name:
                print(Presenter.error("Name is required. Please enter a name."))
                continue
            break

        contact = self.repository.find_contact(name)

        if contact is None:
            contact = Record(name)
            self.repository.add_contact(contact)
        else:
            return Presenter.warning("Contact already exist, please use update to modify")

        # Обработка телефона с повторным вводом при ошибке
        while True:
            phone = input("Phone (optional, format: +380XXXXXXXXX): ").strip()
            if not phone:
                break  # Пропускаем если пусто
            try:
                contact.add_phone(phone)
                break  # Успешно добавлен
            except Exception as e:
                print(Presenter.error(f"Error: {e}. Please try again or press Enter to skip."))
                continue

        # Обработка email с повторным вводом при ошибке
        while True:
            email = input("Email (optional): ").strip()
            if not email:
                break  # Пропускаем если пусто
            try:
                contact.add_email(email)
                break  # Успешно добавлен
            except Exception as e:
                print(Presenter.error(f"Error: {e}. Please try again or press Enter to skip."))
                continue

        address = input("Address (optional): ").strip() or None
        if address:
            contact.set_address(address)

        # Обработка дня рождения с повторным вводом при ошибке
        while True:
            birthday = input("Birthday (optional, dd.mm.yyyy): ").strip()
            if not birthday:
                break  # Пропускаем если пусто
            try:
                contact.set_birthday(birthday)
                break  # Успешно добавлен
            except Exception as e:
                print(Presenter.error(f"Error: {e}. Please try again or press Enter to skip."))
                continue

        return Presenter.success("Contact added.")

    @input_error
    def show_contact(self, name: str):
        """Show a specific contact"""
        contact = self.repository.find_contact(name)
        if contact is None:
            raise KeyError(f"Contact {name} not found.")
        Presenter.print_contacts_table([contact])
        return ""

    @input_error
    def show_all_contacts(self):
        """Show all contacts"""
        contacts = self.repository.get_all_contacts()
        if not contacts:
            return Presenter.warning("No contacts stored.")
        Presenter.print_contacts_table(contacts)
        return "" 

    @input_error
    def change(self, name: str, old_phone: str, new_phone: str) -> str:
        """Change a phone number for a contact"""
        record = self.repository.find_contact(name)
        if record is None:
            raise KeyError(f"Contact {name} not found.")
        record.edit_phone(old_phone, new_phone)
        return Presenter.success(f"Phone number for {name} changed from {old_phone} to {new_phone}.")

    @input_error
    def edit_name(self) -> str:
        """Rename a contact"""
        print(Presenter.info("Let's update contact name. Please enter contact name"))
        while True:
            name = input("Name(required): ").strip()
            if not name:
                print(Presenter.error("Name is required. Please enter a name."))
                continue
            break

        contact = self.repository.find_contact(name)

        if not contact:
            raise KeyError(f"Contact {name} not found.")
        
        while True:
            new_name = input("New name(required): ").strip()
            if not new_name:
                print(Presenter.error("New name is required. Please enter a name."))
                continue
            break

        if self.repository.find_contact(new_name):
            raise ValueError(
                f"Contact {new_name} already exists."
            )

        self.repository.delete_contact(name)
        contact.name.value = new_name
        self.repository.add_contact(contact)

        return Presenter.success(f"Contact name changed from {name} to {new_name}.")

    @input_error
    def delete_contact(self):
        """Delete a contact"""
        print(Presenter.info("Let's delete contact. Please enter contact name"))
        while True:
            name = input("Name(required): ").strip()
            if not name:
                print(Presenter.error("Name is required. Please enter a name."))
                continue
            break

        record = self.repository.find_contact(name)
        if record is None:
            raise KeyError(f"Contact {name} not found.")
        print(Presenter.warning("Do you really want to remove this contact?"))
        response = input("(y/n): ").strip()
        if (response == 'y'):
            self.repository.delete_contact(name)
            return Presenter.success(f"Contact {name} deleted successfully.")
        else:
            return Presenter.info('Cancelled. Returning to main menu.')
        

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
        return Presenter.success(f"Phone {phone} removed from contact {name}.")

    @input_error
    def search_contacts(self, query: str) -> str:
        exact_results = self.repository.search_contacts(query)

        if exact_results:
            print(Presenter.info(f"\nFound {len(exact_results)} contact(s):"))
            Presenter.print_contacts_table(exact_results)
            return ""

        closest = self.repository.search_closest_contacts(query)

        if closest:
            print(Presenter.warning(f"\nNo exact matches for '{query}'."))
            print(Presenter.info("Most similar contacts:"))
            Presenter.print_contacts_table(closest)
            return ""

        return Presenter.warning(f"No contacts found matching '{query}'.")

    @input_error
    def show_birthdays(self, days: str) -> str:
        """Show contacts with birthdays within specified number of days"""
        try:
            days_int = int(days)
        except ValueError:
            raise ValueError(
                f"Invalid number of days: {days}. "
                "Please provide a valid integer."
            )

        results = self.birthday_service.find_near(days_int)

        if not results:
            return Presenter.warning(
                f"No contacts have birthdays in the next {days_int} days."
            )

        lines = [
            Presenter.info(f"Contacts with birthdays in the next {days_int} days:")
        ]
        for result in results:
            contact_info = f"  {result['name']}"
            if result['phone']:
                contact_info += f" - Phone: {result['phone']}"
            if result['email']:
                contact_info += f" - Email: {result['email']}"
            contact_info += (
                f" - Birthday: {result['date']} ({result['weekday']})"
            )
            lines.append(contact_info)

        return "\n".join(lines)

    def _handle_help(self):
        header = Presenter.header("Available Commands:")

        add_info = 'add <name> [phone] [email] [address] [birthday]'
        add_cmd = (
            f"  {Presenter.info(add_info)}\n"
            "    Add or update a contact\n"
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

        birthdays_cmd = (
            f"  {Presenter.info('birthdays <days>')}\n"
            f"    Show contacts with birthdays within "
            f"the specified number of days\n"
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
            + birthdays_cmd
            + system_header
            + help_cmd
            + exit_cmd
            + example
        )

        return help_text
