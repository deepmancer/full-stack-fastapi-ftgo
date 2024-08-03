import pytest
from unittest.mock import AsyncMock, patch
from domain import UserManager
from domain.customer import Customer  # Import the specific user type
from application.address import AddressService


@pytest.fixture
def mock_user():
    user = AsyncMock(spec=Customer)  # Use Customer as the spec
    return user


@pytest.fixture
def mock_load_user(mock_user):
    with patch.object(UserManager, 'load', return_value=mock_user) as mock:
        yield mock


@pytest.mark.asyncio
async def test_add_address(mock_load_user, mock_user):
    mock_user.add_address.return_value = {"address": "mock_address_info"}
    result = await AddressService.add_address(
        user_id="user123",
        latitude=40.7128,
        longitude=-74.0060,
        address_line_1="123 Main St",
        address_line_2="Apt 4",
        city="New York",
        postal_code="10001",
        country="USA"
    )
    assert result == {"address": "mock_address_info"}
    mock_user.add_address.assert_awaited_once_with(
        latitude=40.7128,
        longitude=-74.0060,
        address_line_1="123 Main St",
        address_line_2="Apt 4",
        city="New York",
        postal_code="10001",
        country="USA"
    )


@pytest.mark.asyncio
async def test_get_default_address(mock_load_user, mock_user):
    mock_user.get_default_address_info.return_value = {"address": "mock_default_address"}
    result = await AddressService.get_default_address(user_id="user123")
    assert result == {"address": "mock_default_address"}
    mock_user.get_default_address_info.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_address(mock_load_user, mock_user):
    result = await AddressService.delete_address(user_id="user123", address_id="address123")
    assert result == {}
    mock_user.delete_address.assert_awaited_once_with("address123")


@pytest.mark.asyncio
async def test_set_preferred_address(mock_load_user, mock_user):
    mock_user.set_address_as_default.return_value = {"address": "mock_updated_address"}
    result = await AddressService.set_preferred_address(user_id="user123", address_id="address123")
    assert result == {"address": "mock_updated_address"}
    mock_user.set_address_as_default.assert_awaited_once_with("address123")


@pytest.mark.asyncio
async def test_get_address_info(mock_load_user, mock_user):
    mock_user.get_address_info.return_value = {"address": "mock_address_info"}
    result = await AddressService.get_address_info(user_id="user123", address_id="address123")
    assert result == {"address": "mock_address_info"}
    mock_user.get_address_info.assert_awaited_once_with("address123")




@pytest.mark.asyncio
async def test_update_information(mock_load_user, mock_user):
    mock_user.update_address_information.return_value = {"address": "mock_updated_address"}
    result = await AddressService.update_information(
        user_id="user123",
        address_id="address123",
        update_data={"city": "New City"}
    )
    assert result == {"address": "mock_updated_address"}
    mock_user.update_address_information.assert_awaited_once_with("address123", {"city": "New City"})
