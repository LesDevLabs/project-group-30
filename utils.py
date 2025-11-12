import re


def validate_email(email: str):
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if ((not email) or not bool(email.strip())):
        raise ValueError('Please enter email')

    if (not re.match(email_pattern, email)):
        raise ValueError('Email is not valid')

    return True


def validate_phone_number(phone: str):
    formatted_phone = normalize_phone(phone)

    if (not formatted_phone.isdigit()):
        raise TypeError('Expected only digits')

    if (len(formatted_phone) != 12):
        raise ValueError('Phone number is not full')

    return True


def normalize_phone(phone_number: str):
    if (not bool(phone_number.strip())):
        raise ValueError('Phone number is empty')

    number_pattern = r'\d'
    phone_numbers_list = re.findall(number_pattern, phone_number.replace(' ', ''))
    cleaned_phone_number = ''.join(phone_numbers_list)

    if (len(phone_numbers_list) and phone_numbers_list[0] == '3'):
        return f'{cleaned_phone_number}'
    else:
        return f'38{cleaned_phone_number}'



# ===== UI HELPER FUNCTIONS =====

def show_menu(title: str, options: dict):
    """
    Display a menu with options.
    
    Args:
        title: Menu title
        options: Dictionary of {key: description}
    """
    print(f"\n{title}")
    for key, description in options.items():
        print(f"Enter {key} to {description}")


def get_user_choice(prompt: str = "Your choice: ") -> str:
    """Get user input choice."""
    return input(prompt).strip()


def get_optional_input(prompt: str, skip_value: str = "0") -> str | None:
    """
    Get optional input from user.
    Returns None if user enters skip_value.
    """
    value = input(prompt).strip()
    return None if value == skip_value else value


def confirm_action(prompt: str) -> bool:
    """
    Ask user for confirmation (1 for Yes, 0 for No).
    Returns True if user confirms.
    """
    choice = input(prompt).strip()
    return choice == "1"


# ===== PAGINATION HELPERS =====

def paginate_list(items: list, page: int = 1, page_size: int = 20):
    """
    Paginate a list of items.
    
    Returns:
        tuple: (current_page_items, has_next_page, total_pages)
    """
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    current_items = items[start_idx:end_idx]
    has_next = end_idx < len(items)
    total_pages = (len(items) + page_size - 1) // page_size
    return current_items, has_next, total_pages


def display_numbered_list(items: list, start_number: int = 1):
    """Display a numbered list of items."""
    for idx, item in enumerate(items, start=start_number):
        print(f"{idx}. {item}")
