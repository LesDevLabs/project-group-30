
from handlers.decorators import input_error


class CommandHandler:
    def __init__(self, address_book):
        self.book = address_book
        self.commands = {
            "change": self.change,
            "rename": self.edit_name,
            "delete": self.delete_contact,
            "delete-phone": self.delete_phone,
        }

    @input_error
    def change(self, args: list[str]) -> str:
        if len(args) < 3:
            return "Error: Please provide contact name, old phone, and new phone."

        name, old_phone, new_phone = args
        record = self.book.find(name)
        record.edit_phone(old_phone, new_phone)

        return f"Phone number for {name} changed from {old_phone} to {new_phone}."

    @input_error
    def edit_name(self, args: list[str]) -> str:
        if len(args) < 2:
            return "Error: Please provide old name and new name."

        old_name, new_name = args
        record = self.book.find(old_name)

        if not record:
            return f"Contact {old_name} not found."

        if self.book.find(new_name):
            return f"Contact {new_name} already exists."

        self.book.delete(old_name)
        record.name.value = new_name
        self.book.add_record(record)

        return f"Contact name changed from {old_name} to {new_name}."


    @input_error
    def delete_contact(self, args: list[str]) -> str:
        if len(args) < 1:
            return "Error: Please provide contact name."

        name = args[0]
        record = self.book.find(name)

        if not record:
            return f"Contact {name} not found."

        self.book.delete(name)
        return f"Contact {name} deleted successfully."

    @input_error
    def delete_phone(self, args: list[str]) -> str:
        if len(args) < 2:
            return "Error: Please provide contact name and phone number."

        name, phone = args
        record = self.book.find(name)

        if not record:
            return f"Contact {name} not found."

        phone_obj = record.find_phone(phone)
        if not phone_obj:
            return f"Phone {phone} not found for contact {name}."

        record.remove_phone(phone)
        return f"Phone {phone} removed from contact {name}."
    
    
