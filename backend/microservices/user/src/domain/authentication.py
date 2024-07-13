import pyotp

from config import AccountVerificationConfig

class Authenticator:
    _otp = pyotp.TOTP(
        pyotp.random_base32(),
        digits=AccountVerificationConfig.auth_code_digits_cnt,
        interval=AccountVerificationConfig.auth_code_ttl_sec,
    )

    @staticmethod
    def create_auth_code(user_id: str) -> str:
        auth_code = Authenticator._otp.now()
        return auth_code, Authenticator._otp.interval

    @staticmethod
    def verify_auth_code(auth_code: str) -> bool:
        return Authenticator._otp.verify(auth_code)
