"""
Main command router and orchestrator.
Routes commands to appropriate handlers (contact, task, etc.).
"""
from models.contact import Record
from handlers.decorators import input_error
from handlers.contact_handler import ContactHandler
from handlers.task_handler import TaskHandler


class CommandHandler:
    def __init__(self, contact_repository, task_repository):
        self.contact_repository = contact_repository
        self.task_repository = task_repository
        self.contact_handler = ContactHandler(contact_repository)
        self.task_handler = TaskHandler(task_repository)
        
        # Legacy commands for backward compatibility
        self.commands = {
            "add": self.add_contact,
            "show": self.show_contact,
            "all": self.show_all_contacts,
            "change": self.change,
            "rename": self.edit_name,
            "delete": self.delete_contact,
            "delete-phone": self.delete_phone,
        }

    # ===== ROUTING METHODS =====
    
    def route_add_command(self, args: list):
        """Route add command to appropriate handler."""
        # TODO: Implement routing logic
        pass

    def route_find_command(self, args: list):
        """Route find command to appropriate handler."""
        # TODO: Implement routing logic
        pass

    def route_change_command(self, args: list):
        """Route change command to appropriate handler."""
        # TODO: Implement routing logic
        pass

    def route_delete_command(self, args: list):
        """Route delete command to appropriate handler."""
        # TODO: Implement routing logic
        pass

    def route_all_command(self, args: list):
        """Route all command to show contacts or tasks."""
        # TODO: Implement routing logic
        pass

    def route_sort_command(self, args: list):
        """Route sort command to appropriate handler."""
        # TODO: Implement routing logic
        pass

    # ===== LEGACY METHODS (for backward compatibility) =====

    @input_error
    def add_contact(self, name: str, phone: str = None,
                    email: str = None, address: str = None,
                    birthday: str = None):
        """Add or update a contact (legacy method)"""
        contact = self.contact_repository.find_contact(name)
        if contact is None:
            contact = Record(name)
            self.contact_repository.add_contact(contact)
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
        """Show a specific contact (legacy method)"""
        contact = self.contact_repository.find_contact(name)
        if contact is None:
            raise KeyError(f"Contact {name} not found.")
        return str(contact)

    @input_error
    def show_all_contacts(self):
        """Show all contacts (legacy method)"""
        contacts = self.contact_repository.get_all_contacts()
        if not contacts:
            return "No contacts stored."
        return "\n".join(str(contact) for contact in contacts)

    @input_error
    def change(self, name: str, old_phone: str, new_phone: str) -> str:
        """Change a phone number for a contact (legacy method)"""
        record = self.contact_repository.find_contact(name)
        if record is None:
            raise KeyError(f"Contact {name} not found.")
        record.edit_phone(old_phone, new_phone)
        return (f"Phone number for {name} changed from "
                f"{old_phone} to {new_phone}.")

    @input_error
    def edit_name(self, old_name: str, new_name: str) -> str:
        """Rename a contact (legacy method)"""
        record = self.contact_repository.find_contact(old_name)
        if not record:
            raise KeyError(f"Contact {old_name} not found.")

        if self.contact_repository.find_contact(new_name):
            raise ValueError(f"Contact {new_name} already exists.")

        self.contact_repository.delete_contact(old_name)
        record.name.value = new_name
        self.contact_repository.add_contact(record)

        return f"Contact name changed from {old_name} to {new_name}."

    @input_error
    def delete_contact(self, name: str):
        """Delete a contact (legacy method)"""
        record = self.contact_repository.find_contact(name)
        if record is None:
            raise KeyError(f"Contact {name} not found.")
        self.contact_repository.delete_contact(name)
        return f"Contact {name} deleted successfully."

    @input_error
    def delete_phone(self, name: str, phone: str) -> str:
        """Delete a phone number from a contact (legacy method)"""
        record = self.contact_repository.find_contact(name)
        if not record:
            raise KeyError(f"Contact {name} not found.")

        phone_obj = record.find_phone(phone)
        if not phone_obj:
            raise ValueError(f"Phone {phone} not found for contact {name}.")

        record.remove_phone(phone)
        return f"Phone {phone} removed from contact {name}."
