from models.field import Field


class Phone(Field):
    def __init__(self, value):
        # phone validation here on in repo?
        super().__init__(value)
