import bcrypt

class PasswordHandler:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(raw_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except ValueError:
            return False
