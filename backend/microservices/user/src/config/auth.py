from config.base import BaseConfig, env_var

class AccountVerificationConfig(BaseConfig):
    def __init__(
        self,
        auth_code_ttl_sec: int = None,
        auth_code_digits_cnt: int = None,
    ):
        if auth_code_ttl_sec is None and auth_code_digits_cnt is None:
            config = self.load()
            self.auth_code_ttl_sec = config.auth_code_ttl_sec
            self.auth_code_digits_cnt = config.auth_code_digits_cnt
        else:
            self.auth_code_ttl_sec = auth_code_ttl_sec
            self.auth_code_digits_cnt = auth_code_digits_cnt
        
    @classmethod
    def load(cls):
        return cls(
            auth_code_ttl_sec=env_var("AUTH_CODE_TTL_SEC", default=420, cast_type=int),
            auth_code_digits_cnt=env_var("AUTH_CODE_DIGITS_CNT", default=5, cast_type=int)
        )
