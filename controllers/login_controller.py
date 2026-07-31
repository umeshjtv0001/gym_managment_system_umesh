from dao.user_dao import UserDAO


class LoginController:

    def __init__(self):
        self.user_dao = UserDAO()

    def login(self, username, password):
        """
        Validate username and password.
        Returns True if login is successful, otherwise False.
        """

        if not username.strip():
            return False

        if not password.strip():
            return False

        user = self.user_dao.login(username, password)

        if user:
            return True

        return False
    