from ctypes import Union
from typing import Any, Dict, Optional, Type

from ftgo_utils import enums, uuid_gen, hash_utils, utc_time
from ftgo_utils.errors import ErrorCodes, BaseError

from data_access.repository import DatabaseRepository, CacheRepository
from domain.authentication import Authenticator
from domain import get_logger
from domain.user import User
from domain.driver import Driver
from domain.customer import Customer
from dto import ProfileDTO
from utils import handle_exception


class UserManager:
    @staticmethod
    async def load(
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        role: Optional[str] = None,
        validate_verified: bool = True,
        raise_error_on_missing: bool = True,
        **kwargs,
    ) -> Optional[User]:
        try:
            user_profile = await User.load_profile(user_id=user_id, phone_number=phone_number, role=role, raise_error_on_missing=raise_error_on_missing)
            if not user_profile:
                return None
            user = UserManager._create_user_from_dto(user_profile)
            if validate_verified and not user.is_verified():
                raise BaseError(error_code=ErrorCodes.USER_NOT_VERIFIED_ERROR, payload={"user_id": user.user_id})
            await user.load_private_attributes()
            return user
        except Exception as e:
            payload = {"user_id": user_id, "phone_number": phone_number, "role": role}
            get_logger().error(ErrorCodes.USER_LOAD_ACCOUNT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_LOAD_ACCOUNT_ERROR, payload=payload)

    @staticmethod
    async def register(
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str,
        role: str,
        gender: Optional[str] = None,
        email: Optional[str] = None,
        national_id: Optional[str] = None,
        **kwargs,
    ) -> Optional[tuple]:
        try:
            existing_profile = await User.load_profile(phone_number=phone_number, role=role, raise_error_on_missing=False)
            if existing_profile:
                raise BaseError(error_code=ErrorCodes.ACCOUNT_EXISTS_ERROR, payload={"phone_number": phone_number, "role": role})

            if role != enums.Roles.CUSTOMER.value and not national_id:
                raise BaseError(error_code=ErrorCodes.MISSING_NATIONAL_ID_ERROR, payload={"role": role})

            user_id = uuid_gen.uuid4()
            hashed_password = hash_utils.hash_value(password)

            new_profile = ProfileDTO(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                hashed_password=hashed_password,
                role=role,
                gender=gender,
                email=email,
                national_id=national_id,
                created_at=utc_time.now(),
                verified_at=None,
                last_login_time=None,
            )
            new_profile = await DatabaseRepository.insert(new_profile)

            user = UserManager._create_user_from_dto(new_profile)
            auth_code = await UserManager.generate_auth_code(user.user_id)

            get_logger().info(f"User with user_id: {user_id} and phone_number: {phone_number} was created successfully")
            return user_id, auth_code
        except Exception as e:
            payload = {"phone_number": phone_number, "role": role}
            get_logger().error(ErrorCodes.USER_REGISTRATION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_REGISTRATION_ERROR, payload=payload)

    @staticmethod
    async def verify_account(user_id: str, auth_code: str) -> Optional[User]:
        try:
            user = await UserManager.load(user_id=user_id, validate_verified=False)

            if user.is_verified():
                raise BaseError(error_code=ErrorCodes.USER_ALREADY_VERIFIED_ERROR, payload={"user_id": user.user_id})

            if not Authenticator.verify_auth_code(auth_code):
                raise BaseError(error_code=ErrorCodes.INVALID_AUTHENTICATION_CODE_ERROR, payload={"user_id": user.user_id, "auth_code": auth_code})

            stored_auth_code = await UserManager.fetch_auth_code(user.user_id)

            if stored_auth_code and stored_auth_code == auth_code:
                verified_profile = (await DatabaseRepository.update(
                    ProfileDTO, query={"id": user_id}, update_fields={"verified_at": utc_time.now()}
                ))[0]
                user.verified_at = verified_profile.verified_at
            else:
                raise BaseError(
                    error_code=ErrorCodes.WRONG_AUTHENTICATION_CODE_ERROR,
                    payload={"user_id": user.user_id, "auth_code": auth_code, "stored_auth_code": stored_auth_code},
                )
            return user
        except Exception as e:
            payload = {"user_id": user_id, "auth_code": auth_code}
            get_logger().error(ErrorCodes.USER_VERIFICATION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_VERIFICATION_ERROR, payload=payload)

    @staticmethod
    async def resend_auth_code(user_id: str) -> str:
        try:
            user = await UserManager.load(user_id=user_id, validate_verified=False)
            if user.is_verified():
                raise BaseError(error_code=ErrorCodes.USER_ALREADY_VERIFIED_ERROR, payload={"user_id": user_id})

            current_auth_code = await UserManager.fetch_auth_code(user.user_id)
            if current_auth_code and Authenticator.verify_auth_code(current_auth_code):
                get_logger().info("Resending an existing auth code", payload={"user_id": user_id, "auth_code": current_auth_code})
                return current_auth_code
            auth_code = await UserManager.generate_auth_code(user.user_id)
            return auth_code
        except Exception as e:
            payload = {"user_id": user_id}
            get_logger().error(ErrorCodes.RESENDING_AUTHENTICATION_CODE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.RESENDING_AUTHENTICATION_CODE_ERROR, payload=payload)

    @staticmethod
    async def login(
        password: str,
        role: str,
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> Optional[User]:
        try:
            user = await UserManager.load(phone_number=phone_number, role=role, user_id=user_id)
            if not user or not hash_utils.verify(password, user.hashed_password):
                raise BaseError(
                    error_code=ErrorCodes.WRONG_PASSWORD_ERROR,
                    payload={"user_id": user.user_id if user else None, "password": password},
                )
            user_profile = (await DatabaseRepository.update(ProfileDTO, query={"id": user.user_id}, update_fields={"last_login_time": utc_time.now()}))[0]
            user = UserManager._create_user_from_dto(user_profile)
            return user
        except Exception as e:
            payload = {"user_id": user_id, "phone_number": phone_number, "password": password, "role": role}
            get_logger().error(ErrorCodes.USER_LOGIN_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_LOGIN_ERROR, payload=payload)

    @staticmethod
    def _create_user_from_dto(profile: ProfileDTO) -> Optional[User]:
        if profile.role == enums.Roles.DRIVER.value:
            return Driver.from_dto(profile)
        elif profile.role == enums.Roles.CUSTOMER.value:
            return Customer.from_dto(profile)
        else:
            return User.from_dto(profile)

    @staticmethod
    async def fetch_auth_code(user_id: str) -> Optional[str]:
        try:
            auth_code = await CacheRepository.fetch(user_id)
            if auth_code and Authenticator.verify_auth_code(auth_code):
                return str(auth_code)
            return None
        except Exception as e:
            payload = {"user_id": user_id}
            get_logger().error(ErrorCodes.LOAD_AUTHENTICATION_CODE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.LOAD_AUTHENTICATION_CODE_ERROR, payload=payload)

    @staticmethod
    async def generate_auth_code(user_id: str) -> str:
        try:
            auth_code, ttl = Authenticator.create_auth_code(user_id)
            await CacheRepository.insert(user_id, auth_code, ttl)
            return auth_code
        except Exception as e:
            payload = {"user_id": user_id}
            get_logger().error(ErrorCodes.GENERATE_AUTHENTICATION_CODE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.GENERATE_AUTHENTICATION_CODE_ERROR, payload=payload)
