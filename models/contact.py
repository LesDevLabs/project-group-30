from models.name import Name
from models.phone import Phone
from models.birthday import Birthday
from models.email import Email
from models.address import Address


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.address = None
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def add_email(self, email):
        self.emails.append(Email(email))
    
    def set_address(self, address):
        self.address = Address(address)
    
    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def __str__(self):
        result = f"Contact name: {self.name.value}"
        if self.phones:
            result += f", phones: {'; '.join(p.value for p in self.phones)}"
        if self.emails:
            result += f", emails: {'; '.join(e.value for e in self.emails)}"
        if self.address:
            result += f", address: {self.address.value}"
        if self.birthday:
            result += f", birthday: {self.birthday}"
        return result