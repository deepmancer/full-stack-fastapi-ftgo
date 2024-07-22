from typing import Dict, Any

from domain.user import UserDomain

class ProfileService:
    """
    Service class for managing user profiles.
    """

    @staticmethod
    async def register(
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str,
        role: str,
        national_id: str = None,
    ) -> Dict[str, Any]:
        """
        Registers a new user.

        :param first_name: First name of the user.
        :param last_name: Last name of the user.
        :param phone_number: Phone number of the user.
        :param password: Password for the user account.
        :param role: Role of the user.
        :param national_id: (Optional) National ID of the user.
        :return: Dictionary containing user ID and authentication code.
        """
        user_id, auth_code = await UserDomain.register(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            role=role,
            national_id=national_id,
        )
        return {
            "user_id": user_id,
            "auth_code": auth_code,
        }

    @staticmethod
    async def verify_account(user_id: str, auth_code: str) -> Dict[str, str]:
        """
        Verifies a user account using an authentication code.

        :param user_id: ID of the user.
        :param auth_code: Authentication code for verification.
        :return: Dictionary containing verified user ID.
        """
        verified_user_id = await UserDomain.verify_account(user_id, auth_code.strip())
        return {
            "user_id": verified_user_id,
        }

    @staticmethod
    async def login(phone_number: str, password: str, role: str) -> Dict[str, str]:
        """
        Logs in a user.

        :param phone_number: Phone number of the user.
        :param password: Password of the user.
        :param role: Role of the user.
        :return: Dictionary containing user ID.
        """
        user = await UserDomain.load(phone_number=phone_number, role=role)
        await user.login(password)
        return {
            "user_id": user.user_id,
        }

    @staticmethod
    async def get_info(user_id: str) -> Dict[str, Any]:
        """
        Retrieves user information.

        :param user_id: ID of the user.
        :return: Dictionary containing user information.
        """
        user = await UserDomain.load(user_id=user_id)
        return user.get_info()

    @staticmethod
    async def delete_account(user_id: str) -> Dict[str, str]:
        """
        Deletes a user account.

        :param user_id: ID of the user.
        :return: Dictionary containing user ID.
        """
        user = await UserDomain.load(user_id=user_id)
        await user.delete_account()
        return {
            "user_id": user.user_id,
        }

    @staticmethod
    async def logout(user_id: str) -> Dict[str, str]:
        """
        Logs out a user.

        :param user_id: ID of the user.
        :return: Dictionary containing user ID.
        """
        user = await UserDomain.load(user_id=user_id)
        await user.logout()
        return {
            "user_id": user.user_id,
        }

    @staticmethod
    async def update_profile(user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates user profile information.

        :param user_id: ID of the user.
        :param update_data: Dictionary containing the updated profile information.
        :return: Dictionary containing updated user information.
        """
        user = await UserDomain.load(user_id=user_id)
        return await user.update_profile_information(update_data)

    @staticmethod
    async def get_user_info_with_credentials(user_id: str) -> Dict[str, Any]:
        """
        Retrieves user information along with credentials.

        :param user_id: ID of the user.
        :return: Dictionary containing hashed password and user information.
        """
        user = await UserDomain.load(user_id=user_id)
        user_info = user.get_info()
        return {
            "hashed_password": user.hashed_password,
            **user_info,
        }
