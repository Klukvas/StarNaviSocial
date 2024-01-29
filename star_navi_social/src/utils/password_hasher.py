from src.config import settings


class PasswordHasher:
    @staticmethod
    def get_password_hash(password):
        return settings.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return settings.pwd_context.verify(plain_password, hashed_password)