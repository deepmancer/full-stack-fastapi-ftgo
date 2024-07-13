from config.base import BaseConfig, env_var

class AccountVerificationConfig(BaseConfig):
    auth_code_ttl_sec: int = env_var("AUTH_CODE_TTL_SEC", 420, int)
    auth_code_digits_cnt: int = env_var("AUTH_CODE_DIGITS_CNT", 6, int)

