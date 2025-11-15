from cli.presenter import Presenter
from models.contact import Record
from models.note import Note
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
            "note-add": self.note_add,
            "na": self.note_add,
            "note-del": self.note_del,
            "nd": self.note_del,
            "note-list": self.note_list,
            "nl": self.note_list,
            "ne": self.note_edit,
            "n-edit": self.note_edit,
            "search-contacts": self.search_contacts,
            "birthdays": self.show_birthdays,
            "help": self._handle_help,
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
            return "Contact already exist, please use update to modify"

        # Обработка телефона с повторным вводом при ошибке
        while True:
            phone = input("Phone (optional, format: 380XXXXXXXXX): ").strip()
            if not phone:
                break  # Пропускаем если пусто
            try:
                contact.add_phone(phone)
                break  # Успешно добавлен
            except Exception as e:
                print(f"Error: {e}. Please try again or press Enter to skip.")
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
                print(f"Error: {e}. Please try again or press Enter to skip.")
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
                print(f"Error: {e}. Please try again or press Enter to skip.")
                continue

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
    def change(self) -> str:
        """Change a contact field - displays interactive menu"""
        while True:
            self._display_change_menu()
            choice = input("Enter your choice: ").strip()

            # Allow Enter to cancel
            if not choice:
                return "Return to main menu"

            if choice == "6":
                return "Return to main menu"

            if choice not in ["1", "2", "3", "4", "5"]:
                print("Invalid choice. Please enter a number from 1 to 6.\n")
                continue

            # Get contact name
            while True:
                name = input("Enter the EXISTING contact name to edit: ").strip()
                # Allow Enter to cancel
                if not name:
                    return "Return to main menu"
                break

            contact = self.repository.find_contact(name)
            if contact is None:
                raise KeyError(f"Contact {name} not found.")

            # Handle the selected option
            result = None
            if choice == "1":
                result = self._change_name(contact, name)
            elif choice == "2":
                result = self._change_phone(contact, name)
            elif choice == "3":
                result = self._change_email(contact, name)
            elif choice == "4":
                result = self._change_address(contact, name)
            elif choice == "5":
                result = self._change_birthday(contact, name)

            # Check if user cancelled (returned None)
            if result is None:
                return "Return to main menu"
            return result

    def _display_change_menu(self):
        """Display the change menu options"""
        print("\nChoose what you want to edit:\n")
        print("1. Name")
        print("2. Phone")
        print("3. Email")
        print("4. Address")
        print("5. Birthday")
        print("6. Return\n")

    @input_error
    def _change_name(self, contact: Record, current_name: str) -> str:
        """Handle name editing"""
        print(f"\nCurrent contact name: {current_name}")
        while True:
            new_name = input("Enter the NEW name for this contact: ").strip()
            # Allow Enter to cancel
            if not new_name:
                return None
            break

        if self.repository.find_contact(new_name):
            raise ValueError(f"Contact {new_name} already exists.")

        self.repository.delete_contact(current_name)
        contact.name.value = new_name
        self.repository.add_contact(contact)

        return f"Contact name changed from {current_name} to {new_name}."

    @input_error
    def _change_phone(self, contact: Record, name: str) -> str:
        """Handle phone editing"""
        if not contact.phones:
            print("This contact has no phone numbers.")
            add_new = (
                input("Would you like to add a new phone? (y/n): ").strip().lower()
            )
            # Allow Enter to cancel
            if not add_new:
                return None
            if add_new == "y":
                while True:
                    new_phone = input(
                        "Enter new phone (format: +380XXXXXXXXX): "
                    ).strip()
                    # Allow Enter to cancel
                    if not new_phone:
                        return None
                    try:
                        contact.add_phone(new_phone)
                        return f"Phone {new_phone} added to contact {name}."
                    except Exception as e:
                        print(f"Error: {e}. Please try again.")
                        continue
            else:
                return "No changes made."

        # Display existing phones
        print("\nExisting phone numbers:")
        for idx, phone in enumerate(contact.phones, 1):
            print(f"  {idx}. {phone.value}")

        # Get old phone selection
        while True:
            try:
                selection = input(
                    "\nEnter the number of the phone to edit "
                    "(or enter the phone number directly): "
                ).strip()
                # Allow Enter to cancel
                if not selection:
                    return None
                # Try to parse as index
                try:
                    idx = int(selection)
                    if 1 <= idx <= len(contact.phones):
                        old_phone = contact.phones[idx - 1].value
                        break
                    else:
                        print(
                            f"Invalid selection. Please enter a number "
                            f"between 1 and {len(contact.phones)}."
                        )
                        continue
                except ValueError:
                    # Not a number, treat as phone value
                    old_phone = selection
                    if contact.find_phone(old_phone):
                        break
                    else:
                        print(f"Phone {old_phone} not found. Please try again.")
                        continue
            except Exception as e:
                print(f"Error: {e}. Please try again.")
                continue

        # Get new phone
        while True:
            new_phone = input("Enter new phone (format: +380XXXXXXXXX): ").strip()
            # Allow Enter to cancel
            if not new_phone:
                return None
            try:
                contact.edit_phone(old_phone, new_phone)
                return (
                    f"Phone number for {name} changed from {old_phone} to {new_phone}."
                )
            except Exception as e:
                print(f"Error: {e}. Please try again.")
                continue

    @input_error
    def _change_email(self, contact: Record, name: str) -> str:
        """Handle email editing"""
        if not contact.emails:
            print("This contact has no email addresses.")
            add_new = (
                input("Would you like to add a new email? (y/n): ").strip().lower()
            )
            # Allow Enter to cancel
            if not add_new:
                return None
            if add_new == "y":
                while True:
                    new_email = input("Enter new email: ").strip()
                    # Allow Enter to cancel
                    if not new_email:
                        return None
                    try:
                        contact.add_email(new_email)
                        return f"Email {new_email} added to contact {name}."
                    except Exception as e:
                        print(f"Error: {e}. Please try again.")
                        continue
            else:
                return "No changes made."

        # Display existing emails
        print("\nExisting email addresses:")
        for idx, email in enumerate(contact.emails, 1):
            print(f"  {idx}. {email.value}")

        # Get old email selection
        while True:
            try:
                selection = input(
                    "\nEnter the number of the email to edit "
                    "(or enter the email address directly): "
                ).strip()
                # Allow Enter to cancel
                if not selection:
                    return None
                # Try to parse as index
                try:
                    idx = int(selection)
                    if 1 <= idx <= len(contact.emails):
                        old_email = contact.emails[idx - 1].value
                        break
                    else:
                        print(
                            f"Invalid selection. Please enter a number "
                            f"between 1 and {len(contact.emails)}."
                        )
                        continue
                except ValueError:
                    # Not a number, treat as email value
                    old_email = selection
                    if contact.find_email(old_email):
                        break
                    else:
                        print(f"Email {old_email} not found. Please try again.")
                        continue
            except Exception as e:
                print(f"Error: {e}. Please try again.")
                continue

        # Get new email
        while True:
            new_email = input("Enter new email: ").strip()
            # Allow Enter to cancel
            if not new_email:
                return None
            try:
                contact.edit_email(old_email, new_email)
                return f"Email for {name} changed from {old_email} to {new_email}."
            except Exception as e:
                print(f"Error: {e}. Please try again.")
                continue

    @input_error
    def _change_address(self, contact: Record, name: str) -> str:
        """Handle address editing"""
        if contact.address:
            print(f"Current address: {contact.address.value}")

        new_address = input("Enter new address: ").strip()
        # Allow Enter to cancel
        if not new_address:
            return None
        contact.set_address(new_address)
        return f"Address for {name} updated to: {new_address}."

    @input_error
    def _change_birthday(self, contact: Record, name: str) -> str:
        """Handle birthday editing"""
        if contact.birthday:
            print(f"Current birthday: {contact.birthday}")

        while True:
            birthday = input("Enter new birthday (dd.mm.yyyy): ").strip()
            # Allow Enter to cancel
            if not birthday:
                return None

            try:
                contact.set_birthday(birthday)
                return f"Birthday for {name} updated to: {birthday}."
            except Exception as e:
                print(f"Error: {e}. Please try again.")
                continue

    @input_error
    def edit_name(self) -> str:
        """Rename a contact"""
        print("Let's update contact name. Please enter contact name")
        while True:
            name = input("Name(required): ").strip()
            if not name:
                print("Name is required. Please enter a name.\n")
                continue
            break

        contact = self.repository.find_contact(name)

        if not contact:
            raise KeyError(f"Contact {name} not found.")

        while True:
            new_name = input("New name(required): ").strip()
            if not new_name:
                print("New name is required. Please enter a name.")
                continue
            break

        if self.repository.find_contact(new_name):
            raise ValueError(f"Contact {new_name} already exists.")

        self.repository.delete_contact(name)
        contact.name.value = new_name
        self.repository.add_contact(contact)

        return f"Contact name changed from {name} to {new_name}."

    @input_error
    def delete_contact(self):
        """Delete a contact"""
        print("Let's delete contact name. Please enter contact name")
        while True:
            name = input("Name(required): ").strip()
            if not name:
                print("Name is required. Please enter a name.\n")
                continue
            break

        record = self.repository.find_contact(name)
        if record is None:
            raise KeyError(f"Contact {name} not found.")
        print("Let's delete contact name. Please enter contact name")
        response = input("Do you really want to remove contact? (y/n): ").strip()
        if response == "y":
            self.repository.delete_contact(name)
            return f"Contact {name} deleted successfully."
        else:
            return "Return to main menu"

    @input_error
    def delete_phone(self) -> str:
        """Delete a phone number from a contact"""
        print("Let's delete phone number from contact. Please enter contact name")
        while True:
            name = input("Name(required): ").strip()
            if not name:
                print("Name is required. Please enter a name.\n")
                continue
            break
        record = self.repository.find_contact(name)
        if not record:
            raise KeyError(f"Contact {name} not found.")

        while True:
            phone = input("Phone(required): ").strip()
            if not phone:
                print("Phone is required. Please enter a value.\n")
                continue
            break

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
            lines = [f"No exact matches for '{query}':", "Most similar contacts:"]
            lines.extend(str(contact) for contact in closest)
            return "\n".join(lines)

        return f"No contacts found matching '{query}'."

    @input_error
    def show_birthdays(self, days: str) -> str:
        """Show contacts with birthdays within specified number of days"""
        try:
            days_int = int(days)
        except ValueError:
            raise ValueError(
                f"Invalid number of days: {days}. Please provide a valid integer."
            )

        results = self.birthday_service.find_near(days_int)

        if not results:
            return f"No contacts have birthdays in the next {days_int} days."

        lines = [f"Contacts with birthdays in the next {days_int} days:"]
        for result in results:
            contact_info = f"  {result['name']}"
            if result["phone"]:
                contact_info += f" - Phone: {result['phone']}"
            if result["email"]:
                contact_info += f" - Email: {result['email']}"
            contact_info += f" - Birthday: {result['date']} ({result['weekday']})"
            lines.append(contact_info)

        return "\n".join(lines)

    @input_error
    def note_add(self, text=None, tags=None):
        while not text:
            text = input("Enter text: ").strip()

        if tags is None:
            raw = input("Enter tags (comma-separated, optional): ").strip()
            if raw:
                tags = [t.strip() for t in raw.split(",") if t.strip()]
            else:
                tags = []
        else:
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",") if t.strip()]

        note = Note(text, tags)

        return self.repository.add_note(note)

    @input_error
    def note_del(self, query=None):
        while not query:
            query = input("Enter a search string: ").strip()

        note = self.repository.find_note(query)

        if not note:
            return f"Note {query} not found"

        return self.repository.del_note(note)

    @input_error
    def note_list(self, query=None):
        notes = self.repository.search_notes(query)

        if notes and not query:
            print("Use n-list <string> for filter notes")

        return self.repository.format_notes(notes)

    @input_error
    def note_edit(self, query=None):
        while not query:
            query = input("Enter a search string: ").strip()

        note = self.repository.find_note(query)
        if not note:
            return f"Note {query} not found"

        print(f"Edit note {note.text}")
        new_text = None
        while not new_text:
            new_text = input("Enter a new text: ").strip()

        return self.repository.edit_note(note, new_text)

    def _handle_help(self):
        header = Presenter.header("Available Commands:")

        add_info = "add <name> [phone] [email] [address] [birthday]"
        add_cmd = f"  {Presenter.info(add_info)}\n    Add or update a contact\n"

        show_cmd = f"  {Presenter.info('show <name>')}\n    Show a specific contact\n"

        all_cmd = f"  {Presenter.info('all')}\n    Show all contacts\n"

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

        delete_cmd = f"  {Presenter.info('delete <name>')}\n    Delete a contact\n"

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

        help_cmd = f"  {Presenter.info('help [command]')}\n    Show this help message\n"

        exit_cmd = (
            f"  {Presenter.info('exit / quit / close')}\n    Exit the application\n"
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
