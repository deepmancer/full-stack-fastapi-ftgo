from config.base import BaseConfig, env_var

class AccountVerificationConfig(BaseConfig):
    def __init__(
        self,
        auth_code_ttl_sec: int = None,
        auth_code_digits_cnt: int = None,
    ):
        self.auth_code_ttl_sec = auth_code_ttl_sec or env_var("AUTH_CODE_TTL_SEC", default=420, cast_type=int)
        self.auth_code_digits_cnt = auth_code_digits_cnt or env_var("AUTH_CODE_DIGITS_CNT", default=5, cast_type=int)
