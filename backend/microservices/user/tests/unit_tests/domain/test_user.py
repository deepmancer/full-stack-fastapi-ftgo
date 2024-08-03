import pytest
from unittest.mock import MagicMock, patch
from domain.user import User
from dto import ProfileDTO

@pytest.fixture
def user():
    return User(
        user_id="123",
        role="admin",
        first_name="John",
        last_name="Doe",
        phone_number="1234567890",
        hashed_password="hashed_password",
        gender="male",
        email="john.doe@example.com",
        created_at=None,
        verified_at=None,
        last_login_time=None,
        national_id="123456789",
    )

@pytest.mark.asyncio
async def test_load_profile_user_found(user):
    # Mock the DatabaseRepository.fetch method to return a user profile
    mock_profile = ProfileDTO(
        user_id="123",
        first_name="John",
        last_name="Doe",
        phone_number="1234567890",
        hashed_password="hashed_password",
        gender="male",
        email="john.doe@example.com",
        created_at=None,
        verified_at=None,
        last_login_time=None,
        national_id="123456789",
    )
    with patch("domain.user.DatabaseRepository.fetch", return_value=mock_profile):
        profile = await user.load_profile(user_id="123", raise_error_on_missing=False)
        assert profile == mock_profile

@pytest.mark.asyncio
async def test_load_profile_user_not_found(user):
    # Mock the DatabaseRepository.fetch method to return None
    with patch("domain.user.DatabaseRepository.fetch", return_value=None):
        profile = await user.load_profile(user_id="123", raise_error_on_missing=False)
        assert profile is None

@pytest.mark.asyncio
async def test_logout(user):
    # Mock the CacheRepository.delete method
    with patch("domain.user.CacheRepository.delete") as mock_delete:
        await user.logout()
        mock_delete.assert_called_once_with(user.user_id)

@pytest.mark.asyncio
async def test_delete_account(user):
    # Mock the DatabaseRepository.delete and CacheRepository.delete methods
    with patch("domain.user.DatabaseRepository.delete") as mock_delete, \
         patch("domain.user.CacheRepository.delete") as mock_cache_delete:
        await user.delete_account()
        mock_delete.assert_called_once_with(ProfileDTO, query={"id": user.user_id})
        mock_cache_delete.assert_called_once_with(user.user_id)

@pytest.mark.asyncio
async def test_update_profile_information(user):
    update_fields = {
        "first_name": "Jane",
        "last_name": "Smith",
        "phone_number": "9876543210",
        "email": "jane.smith@example.com",
        "gender": "female",
        "national_id": "987654321",
    }
    updated_profile = ProfileDTO(
        user_id="123",
        first_name="Jane",
        last_name="Smith",
        phone_number="9876543210",
        hashed_password="hashed_password",
        gender="female",
        email="jane.smith@example.com",
        created_at=None,
        verified_at=None,
        last_login_time=None,
        national_id="987654321",
    )
    with patch("domain.user.DatabaseRepository.update", return_value=[updated_profile]):
        result = await user.update_profile_information(update_fields)
        assert result == user.get_info()

def test_get_info(user):
    info_dict = {
        "user_id": "123",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "1234567890",
        "hashed_password": "hashed_password",
        "gender": "male",
        "email": "john.doe@example.com",
        "national_id": "123456789",
        "role": "admin",
    }
    assert user.get_info() == info_dict

def test_is_verified(user):
    assert user.is_verified() == False

def test_update_from_dto(user):
    profile = ProfileDTO(
        user_id="123",
        first_name="Jane",
        last_name="Smith",
        phone_number="9876543210",
        hashed_password="hashed_password",
        gender="female",
        email="jane.smith@example.com",
        created_at=None,
        verified_at=None,
        last_login_time=None,
        national_id="987654321",
    )
    user.update_from_dto(profile)
    assert user.first_name == "Jane"
    assert user.last_name == "Smith"
    assert user.phone_number == "9876543210"
    assert user.email == "jane.smith@example.com"
    assert user.gender == "female"
    assert user.national_id == "987654321"

def test_from_dto(user):
    profile = ProfileDTO(
        user_id="123",
        first_name="Jane",
        last_name="Smith",
        phone_number="9876543210",
        hashed_password="hashed_password",
        gender="female",
        email="jane.smith@example.com",
        created_at=None,
        verified_at=None,
        last_login_time=None,
        national_id="987654321",
    )
    new_user = User.from_dto(profile)
    assert new_user.user_id == "123"
    assert new_user.first_name == "Jane"
    assert new_user.last_name == "Smith"
    assert new_user.phone_number == "9876543210"
    assert new_user.email == "jane.smith@example.com"
    assert new_user.gender == "female"
    assert new_user.national_id == "987654321"

@pytest.mark.asyncio
async def test_load_private_attributes(user):
    # No need to test this method as it is empty
    await user.load_private_attributes()

def test_to_dict(user):
    info_dict = {
        "user_id": "123",
        "role": "admin",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "1234567890",
        "hashed_password": "hashed_password",
        "national_id": "123456789",
        "gender": "male",
        "email": "john.doe@example.com",
        "created_at": None,
        "verified_at": None,
        "last_login_time": None,
    }
    assert user.to_dict() == info_dict