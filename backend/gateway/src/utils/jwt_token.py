import jwt
import datetime
from typing import Optional, Dict, Any, List
import jwt.exceptions as jwt_errors
from config.timezone import tz

class JWTTokenHandler:
    @staticmethod
    def encode(payload: Dict[str, Any], secret: str, algorithm: str, expiration: Optional[int] = None, **kwargs) -> str:

        if expiration:
            payload['exp'] = datetime.datetime.now(tz=tz) + datetime.timedelta(seconds=expiration)
        payload.update(kwargs)
        token = jwt.encode(payload, secret, algorithm=algorithm)
        return token

    @staticmethod
    def decode(token: str, secret: str, algorithms: Optional[List[str]] = None, verify: bool = True, **kwargs) -> Dict[str, Any]:
        try:
            decoded = jwt.decode(token, secret, algorithms=algorithms, options={'verify_signature': verify}, **kwargs)
            return decoded
        except jwt_errors.ExpiredSignatureError:
            raise jwt_errors.ExpiredSignatureError("The token has expired.")
        except jwt_errors.InvalidTokenError as e:
            raise jwt_errors.InvalidTokenError(f"Invalid token: {str(e)}")
