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
            "find" : self.search_contacts
        }

    @input_error
    def add_contact(self, name: str, phone: str = None,
                    email: str = None, address: str = None,
                    birthday: str = None):
        """Add or update a contact"""
        contact = self.repository.find_contact(name)
        if contact is None:
            contact = Record(name)
            self.repository.add_contact(contact)
            message = "Contact added."
        else:
            message = "Contact updated."

        if phone:
            contact.add_phone(phone)
        if email:
            contact.add_email(email)
        if address:
            contact.set_address(address)
        if birthday:
            contact.set_birthday(birthday)

        return message

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
        return (f"Phone number for {name} changed from "
                f"{old_phone} to {new_phone}.")

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