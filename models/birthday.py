from models.field import Field
from datetime import datetime
from handlers.errors import ValidationError


class Birthday(Field):
    # DD.MM.YYYY format
    def __init__(self, value):
        try:
            birth_date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
        # Validate that birthday is not in the future
        if birth_date.date() > datetime.now().date():
            raise ValidationError('birthday', 'Birthday cannot be in the future')
        
        self.value = birth_date
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

