from werkzeug.security import generate_password_hash, check_password_hash


class EncryptionService:
    def is_same_password(self, user_password, password):
        return check_password_hash(user_password, password)

    def hash_password(self, password):
        return generate_password_hash(password, method='sha256')
