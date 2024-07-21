from ftgo_utils import class_property

from config.base import BaseConfig, env_var

class AccountVerificationConfig(BaseConfig):
    @class_property
    def auth_code_ttl_sec(cls):
        return env_var("AUTH_CODE_TTL_SEC", 420, int)
    @class_property
    def auth_code_digits_cnt(cls):
        return env_var("AUTH_CODE_DIGITS_CNT", 6, int)
