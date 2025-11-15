from handlers.errors import ValidationError
from cli.presenter import Presenter


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return Presenter.error(f"Validation Error: {e}")
        except KeyError as e:
            return Presenter.error(f"Error: {e}")
        except ValueError as e:
            return Presenter.error(f"ValueError: {e}")
        except AttributeError:
            return Presenter.error("Error: Contact not found.")
        except Exception as e:
            return Presenter.error(f"Unexpected Error: {e}")
    return wrapper
