from models.contact import Record
from repositories.contact_repository import ContactRepository


class ContactService:
    """Service layer for contact business logic"""

    def __init__(self, repository: ContactRepository):
        self.repository = repository

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

    def show_contact(self, name: str):
        """Show a specific contact"""
        contact = self.repository.find_contact(name)
        if contact is None:
            raise KeyError
        return str(contact)

    def show_all_contacts(self):
        """Show all contacts"""
        contacts = self.repository.get_all_contacts()
        if not contacts:
            return "No contacts stored."
        return "\n".join(str(contact) for contact in contacts)

    def delete_contact(self, name: str):
        """Delete a contact"""
        if self.repository.delete_contact(name):
            return "Contact deleted."
        raise KeyError

