import datetime
from typing import Any, Dict, Optional

from ftgo_utils.errors import ErrorCodes, BaseError
from ftgo_utils import utc_time

from domain import get_logger
from domain.authentication import Authenticator
from data_access.repository import DatabaseRepository, CacheRepository
from dto import ProfileDTO
from utils import handle_exception

class User:
    def __init__(
        self,
        user_id: str,
        role: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        hashed_password: str,
        gender: Optional[str] = None,
        email: Optional[str] = None,
        created_at: Optional[datetime.datetime] = None,
        verified_at: Optional[datetime.datetime] = None,
        last_login_time: Optional[datetime.datetime] = None,
        national_id: Optional[str] = None,
    ):
        self.user_id = user_id
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.hashed_password = hashed_password
        self.gender = gender
        self.email = email
        self.created_at = created_at
        self.verified_at = verified_at
        self.last_login_time = last_login_time
        self.national_id = national_id

    
    @staticmethod
    async def load_profile(
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        role: Optional[str] = None,
        raise_error_on_missing: bool = True,
        **kwargs,
    ) -> Optional[ProfileDTO]:
        query_dict = {}
        if user_id:
            query_dict["id"] = user_id
        if phone_number:
            query_dict["phone_number"] = phone_number
        if role:
            query_dict["role"] = role
        
        try:
            user_profile = await DatabaseRepository.fetch(ProfileDTO, query=query_dict, one_or_none=True)
            if not user_profile:
                if raise_error_on_missing:
                    raise BaseError(error_code=ErrorCodes.USER_NOT_FOUND_ERROR, payload=query_dict)
                return None
            return user_profile
        except Exception as e:
            payload = {"query": query_dict}
            get_logger().error(ErrorCodes.USER_LOAD_PROFILE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_LOAD_PROFILE_ERROR, payload=payload)

    async def logout(self) -> None:
        try:
            await CacheRepository.delete(self.user_id)
        except Exception as e:
            payload = {"user_id": self.user_id}
            get_logger().error(ErrorCodes.USER_LOGOUT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_LOGOUT_ERROR, payload=payload)

    async def delete_account(self) -> None:
        try:
            await DatabaseRepository.delete(ProfileDTO, query={"id": self.user_id})
            await CacheRepository.delete(self.user_id)
        except Exception as e:
            payload = {"user_id": self.user_id}
            get_logger().error(ErrorCodes.USER_DELETE_ACCOUNT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_DELETE_ACCOUNT_ERROR, payload=payload)

    async def update_profile_information(self, update_fields: Dict[str, Optional[str]]) -> Dict[str, Any]:
        new_fields = {}
        if "first_name" in update_fields:
            new_fields["first_name"] = update_fields["first_name"]
        if "last_name" in update_fields:
            new_fields["last_name"] = update_fields["last_name"]
        if "phone_number" in update_fields:
            new_fields["phone_number"] = update_fields["phone_number"]
        if "email" in update_fields:
            new_fields["email"] = update_fields["email"]
        if "gender" in update_fields:
            new_fields["gender"] = update_fields["gender"]
        if "national_id" in update_fields:
            new_fields["national_id"] = update_fields["national_id"]

        if not new_fields:
            return

        try:
            updated_profile = (await DatabaseRepository.update(
                ProfileDTO,
                query={"id": self.user_id},
                update_fields=new_fields,
            ))[0]
            if updated_profile:
                self.update_from_dto(updated_profile)
            return self.get_info()
        except Exception as e:
            payload = {"user_id": self.user_id, "update_fields": update_fields}
            get_logger().error(ErrorCodes.USER_PROFILE_UPDATE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_PROFILE_UPDATE_ERROR, payload=payload)
    
    def get_info(self) -> Dict[str, Any]:
        info_dict = {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "hashed_password": self.hashed_password,
            "gender": self.gender,
            "email": self.email,
            "national_id": self.national_id,
            "role": self.role,
        }
        return {key: value for key, value in info_dict.items() if value is not None}

    def is_verified(self) -> bool:
        return self.verified_at is not None

    def update_from_dto(self, profile: ProfileDTO) -> None:
        self.__init__(**profile.to_dict())

    @classmethod
    def from_dto(cls, profile: ProfileDTO) -> "User":
        return cls(
            user_id=str(profile.user_id),
            first_name=profile.first_name,
            last_name=profile.last_name,
            phone_number=profile.phone_number,
            hashed_password=profile.hashed_password,
            national_id=profile.national_id,
            gender=profile.gender,
            role=profile.role,
            email=profile.email,
            created_at=profile.created_at.astimezone(utc_time.timezone) if profile.created_at else None,
            verified_at=profile.verified_at.astimezone(utc_time.timezone) if profile.verified_at else None,
            last_login_time=profile.last_login_time.astimezone(utc_time.timezone) if profile.last_login_time else None,
        )

    async def load_private_attributes(self) -> None:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "role": self.role,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "hashed_password": self.hashed_password,
            "national_id": self.national_id,
            "gender": self.gender,
            "email": self.email,
            "created_at": self.created_at,
            "verified_at": self.verified_at,
            "last_login_time": self.last_login_time,
        }
