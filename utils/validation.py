import re

class Validation:

    @staticmethod
    def is_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    @staticmethod
    def is_phone(phone):
        return phone.isdigit() and len(phone) == 10

    @staticmethod
    def required(value):
        return value.strip() != ""