from handlers.errors import ValidationError


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {e}"
        except AttributeError:
            return "Error: Contact not found."
        except Exception as e:
            return f"Error: {e}"
        except ValidationError as e:
            return f"Error: {e}"
    return wrapper
