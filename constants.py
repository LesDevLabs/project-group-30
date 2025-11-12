"""
Constants for bot messages, menus, and prompts.
Keeps all user-facing text in one place for easy maintenance.
"""

# ===== WELCOME & HELP MESSAGES =====

WELCOME_MESSAGE = """
=================================================
Welcome to the Contact & Task Assistant Bot!
=================================================
Type "help" for available commands.
"""

GREETING_PROMPT = 'Please say "hello" to start.'

START_MESSAGE = """
How can I help you? You can add, change, or view contacts.
Type "help" for assistance.
"""

GOODBYE_MESSAGE = "Good bye! Have a great day!"

# ===== MENU OPTIONS =====

ADD_MENU = {
    "1": "add a contact",
    "2": "add a task"
}

FIND_MENU = {
    "1": "find a contact",
    "2": "find a contact by address",
    "3": "find a task",
    "4": "find near birthday"
}

CHANGE_CONTACT_MENU = {
    "1": "change name, phone number, email and birthday",
    "2": "change address"
}

CHANGE_TASK_MENU = {
    "1": "change task text",
    "2": "change tags",
    "3": "change and add contact to this task"
}

SORT_TASKS_MENU = {
    "1": "sort by A-Z",
    "2": "sort by Z-A",
    "3": "sort by creation date (newest first)",
    "4": "sort by creation date (oldest first)"
}

SORT_CONTACTS_MENU = {
    "1": "sort by A-Z",
    "2": "sort by Z-A"
}

ALL_MENU = {
    "1": "show all contacts",
    "2": "show all tasks"
}

# ===== INPUT PROMPTS =====

PROMPTS = {
    # Contact prompts
    "contact_name": "Enter Name: ",
    "contact_phone": "Enter phone number (e.g., +380676456767): ",
    "contact_email": "Enter email (enter 0 to pass): ",
    "contact_birthday": "Enter birthday date (enter 0 to pass): ",
    "add_address": "Do you want to add the address? (Enter 1 to Yes or 0 to No): ",
    
    # Address prompts
    "address_country": "Enter Country (enter 0 to pass): ",
    "address_postcode": "Enter Postcode (enter 0 to pass): ",
    "address_city": "Enter City (enter 0 to pass): ",
    "address_line": "Enter Address line (enter 0 to pass): ",
    "address_exit": "Enter new {field} (enter 0 to pass or 00 to exit): ",
    
    # Task prompts
    "task_text": "Enter text (Enter @ContactName to add this task to Contact): ",
    "task_tags": "Enter tags, e.g., #tag1, #tag2... (enter 0 to pass): ",
    
    # Search prompts
    "search_contact": "Enter any information about contact (Name, phone, email): ",
    "search_address": "Enter any information about address (Country, Address, postcode, city): ",
    "search_task": "Enter tag (#tag) or any information about task: ",
    "search_birthday": "Enter number of days or specific date: ",
    
    # Action prompts
    "select_contact": "Enter the contact number to select a specific one: ",
    "contact_action": 'Type "change" to edit, "delete" to remove, or "task" to view related tasks: ',
    "task_action": 'Type "change" to edit or "delete" to remove: ',
    "change_fields": 'Enter fields to change (email, name, phone, birthday) separated by ",": ',
    "link_contact": "Enter contact name: ",
    
    # Pagination
    "pagination": 'Enter number, "sort" to sort, or "next" for next page: ',
}

# ===== SUCCESS MESSAGES =====

SUCCESS = {
    "contact_added": "Contact {name} added successfully!",
    "task_added": "Task added successfully!",
    "contact_updated": "Contact updated.",
    "task_updated": "Task updated.",
    "contact_deleted": "Contact deleted.",
    "task_deleted": "Task deleted.",
    "address_updated": "Address updated.",
    "tags_updated": "Tags updated.",
    "task_linked": "Task linked to contact.",
    "phone_changed": "Phone changed.",
    "name_changed": "Name changed.",
    "email_changed": "Email changed.",
    "birthday_changed": "Birthday changed.",
}

# ===== ERROR MESSAGES =====

ERRORS = {
    "name_required": "Name is required.",
    "phone_required": "Phone is required.",
    "task_text_required": "Task text is required.",
    "invalid_choice": "Invalid choice.",
    "invalid_action": "Invalid action.",
    "cancelled": "{action} cancelled.",
}
