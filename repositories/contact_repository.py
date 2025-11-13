from models.contact import Record

from models.contact import Record


class ContactRepository:
    def __init__(self):
        self.contacts = {}

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
    
    def search_contacts(self, query: str) -> list:
        """
        Search contacts by name, phone, or email
        
        Args:
            query: Search query string
            
        Returns:
            List of matching Record objects
        """
        query_lower = query.lower()
        results = []
        
        for contact in self.contacts.values():
            # Search by name
            if query_lower in contact.name.value.lower():
                results.append(contact)
                continue
            
            # Search by phone
            for phone in contact.phones:
                if query_lower in phone.value.lower():
                    results.append(contact)
                    break
            
            # Search by email
            for email in contact.emails:
                if query_lower in email.value.lower():
                    results.append(contact)
                    break
        
        return results