# models/user.py

class User:
    def __init__(self, id=None, username="", password="", role="admin"):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            password=data.get("password"),
            role=data.get("role", "admin")
        )

    def __str__(self):
        return f"User(ID={self.id}, Username={self.username}, Role={self.role})"