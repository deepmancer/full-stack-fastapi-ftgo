import pyotp

from config.auth import AUTH_CODE_TTL_SECONDS, AUTH_CODE_DIGITS_CNT

class Authenticator:
    _otp = pyotp.TOTP(
        pyotp.random_base32(),
        digits=AUTH_CODE_DIGITS_CNT,
        interval=AUTH_CODE_TTL_SECONDS,
    )

    @staticmethod
    def create_auth_code(user_id: str) -> str:
        auth_code = Authenticator._otp.now()
        return auth_code, Authenticator._otp.interval

    @staticmethod
    def verify_auth_code(auth_code: str) -> bool:
        return Authenticator._otp.verify(auth_code)
