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
