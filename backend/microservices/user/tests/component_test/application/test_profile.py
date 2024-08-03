import pytest
from unittest.mock import AsyncMock, patch
from application.profile import ProfileService

@pytest.mark.asyncio
async def test_register():
    with patch('application.profile.UserManager.register', new_callable=AsyncMock) as mock_register:
        mock_register.return_value = ("user_id_123", "auth_code_123")
        result = await ProfileService.register(
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            password="password",
            role="customer",
        )
        assert result == {"user_id": "user_id_123", "auth_code": "auth_code_123"}
        mock_register.assert_called_once_with(
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            password="password",
            role="customer",
            gender=None,
            email=None,
            national_id=None,
        )

@pytest.mark.asyncio
async def test_resend_auth_code():
    with patch('application.profile.UserManager.resend_auth_code', new_callable=AsyncMock) as mock_resend_auth_code:
        mock_resend_auth_code.return_value = "auth_code_123"
        result = await ProfileService.resend_auth_code("user_id_123")
        assert result == {"user_id": "user_id_123", "auth_code": "auth_code_123"}
        mock_resend_auth_code.assert_called_once_with("user_id_123")


@pytest.mark.asyncio
async def test_delete_account():
    with patch('application.profile.UserManager.load', new_callable=AsyncMock) as mock_load:
        mock_user = AsyncMock()
        mock_load.return_value = mock_user
        result = await ProfileService.delete_account("user_id_123")
        assert result == {}
        mock_load.assert_called_once_with(user_id="user_id_123")
        mock_user.delete_account.assert_called_once()

@pytest.mark.asyncio
async def test_logout():
    with patch('application.profile.UserManager.load', new_callable=AsyncMock) as mock_load:
        mock_user = AsyncMock()
        mock_load.return_value = mock_user
        result = await ProfileService.logout("user_id_123")
        assert result == {}
        mock_load.assert_called_once_with(user_id="user_id_123")
        mock_user.logout.assert_called_once()

@pytest.mark.asyncio
async def test_update_profile():
    with patch('application.profile.UserManager.load', new_callable=AsyncMock) as mock_load:
        mock_user = AsyncMock()
        mock_user.update_profile_information.return_value = {"user_id": "user_id_123", "status": "updated"}
        mock_load.return_value = mock_user
        result = await ProfileService.update_profile("user_id_123", {"email": "new_email@example.com"})
        assert result == {"user_id": "user_id_123", "status": "updated"}
        mock_load.assert_called_once_with(user_id="user_id_123")
        mock_user.update_profile_information.assert_called_once_with({"email": "new_email@example.com"})
