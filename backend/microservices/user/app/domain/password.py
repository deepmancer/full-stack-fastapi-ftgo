import bcrypt

class PasswordHandler:
    @staticmethod
    def hash_password(password: str):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(
            password=password.encode(
                encoding="utf-8",
            ),
            salt=salt,
        ).decode("utf-8")

    @staticmethod
    def verify_password(raw_password: str, hashed_password: str):
        return bcrypt.checkpw(
            password=raw_password.encode(
                encoding="utf-8",
            ),
            hashed_password=hashed_password.encode(
                encoding="utf-8",
            ),
        )
