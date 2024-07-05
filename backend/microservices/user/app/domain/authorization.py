import jwt
import datetime
from typing import Optional
from jwt import PyJWTError
import asyncio
import hashlib

from config.access_token import ACCESS_TOKEN_TTL_SEC, ALGORITHM
from config.timezone import UTC

class TokenHandler:
    @staticmethod
    def _generate_secret_key(user_id: str, user_secret: str) -> str:
        combined_key = f"{user_id}{user_secret}"
        user_specific_secret = hashlib.sha256(combined_key.encode()).hexdigest()
        return user_specific_secret

    @staticmethod
    def generate_token(user_id: str, user_secret: str) -> str:
        try:
            expire = datetime.datetime.now(UTC) + datetime.timedelta(seconds=ACCESS_TOKEN_TTL_SEC)
            to_encode = {"sub": user_id, "exp": expire}
            user_specific_secret = TokenHandler._generate_secret_key(user_id, user_secret)
            encoded_jwt = jwt.encode(to_encode, user_specific_secret, algorithm=ALGORITHM)
            return encoded_jwt, TokenHandler.get_token_ttl(encoded_jwt)
        except Exception as e:
            raise Exception("Token generation failed") from e

    @staticmethod
    def get_token_ttl(token: str) -> int:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            expire = datetime.datetime.fromtimestamp(payload["exp"], UTC)
            ttl = expire - datetime.datetime.now(UTC)
            return ttl.seconds
        except PyJWTError:
            return 0
        except Exception as e:
            raise Exception("Token ttl retrieval failed") from e

    @staticmethod
    def validate_token(user_id: str, user_secret: str, token: str) -> bool:
        try:
            user_specific_secret = TokenHandler._generate_secret_key(user_id, user_secret)
            payload = jwt.decode(token, user_specific_secret, algorithms=[ALGORITHM])
            token_user_id: str = payload.get("sub")
            if token_user_id is None or token_user_id != user_id:
                return False
            if datetime.datetime.now(UTC) > datetime.datetime.fromtimestamp(payload["exp"], UTC):
                return False
            return True
        except PyJWTError:
            return False
        except Exception as e:
            raise Exception("Token validation failed") from e
