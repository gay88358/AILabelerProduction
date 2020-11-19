class UserCredential:
    def get_user_name(self):
        return "admin"

    def get_user_password(self):
        return "webUILabeler"

    def get_name(self):
        return "admin"

    def get_email(self):
        return "gay88358@yahoo.com.tw"

# Singleton design pattern
user_credential = UserCredential()

__all__ = ["user_credential"]
