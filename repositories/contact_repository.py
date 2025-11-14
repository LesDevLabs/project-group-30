from models.contact import Record

from models.contact import Record
from search.search_service import SearchService


class ContactRepository:
    def __init__(self):
        self.contacts = {}
        self.search_service = SearchService()

    def add_contact(self, record: Record):
        """Add a new contact or update existing one"""
        self.contacts[record.name.value] = record

    def find_contact(self, name: str) -> Record:
        """Find a contact by name"""
        return self.contacts.get(name)

    def delete_contact(self, name: str):
        """Delete a contact by name"""
        if name in self.contacts:
            del self.contacts[name]
            return True
        return False

    def get_all_contacts(self):
        """Get all contacts"""
        return list(self.contacts.values())

    def has_contact(self, name: str) -> bool:
        """Check if contact exists"""
        return name in self.contacts
    
    def search_contacts(self, query: str):
        return self.search_service.exact_search(self.contacts, query)


    def search_closest_contacts(self, query: str):
        return self.search_service.fuzzy_search(self.contacts, query)


