import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from domain.assets.address import AddressDomain
from ftgo_utils.errors import BaseError, ErrorCodes
from dto import AddressDTO
from data_access.repository import DatabaseRepository


@pytest.mark.asyncio
async def test_load_success():
    address_data = AddressDTO(
        address_id="address_id_123",
        user_id="user_id_123",
        latitude=10.0,
        longitude=20.0,
        address_line_1="123 Main St",
        address_line_2="Apt 4",
        city="City",
        postal_code="12345",
        country="Country",
        is_default=True,
        created_at=None,
    )

    with patch('data_access.repository.DatabaseRepository.fetch', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = address_data

        address = await AddressDomain.load("user_id_123", "address_id_123")

        assert address is not None
        assert address.address_id == "address_id_123"
        assert address.user_id == "user_id_123"
        mock_fetch.assert_called_once_with(AddressDTO, query={"id": "address_id_123"}, one_or_none=True)


@pytest.mark.asyncio
async def test_load_not_found():
    with patch('data_access.repository.DatabaseRepository.fetch', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = None

        with pytest.raises(BaseError) as exc_info:
            await AddressDomain.load("user_id_123", "address_id_123")

        assert exc_info.value.error_code == ErrorCodes.ADDRESS_NOT_FOUND_ERROR
        mock_fetch.assert_called_once_with(AddressDTO, query={"id": "address_id_123"}, one_or_none=True)


@pytest.mark.asyncio
async def test_load_permission_denied():
    address_data = AddressDTO(
        address_id="address_id_123",
        user_id="other_user_id",
        latitude=10.0,
        longitude=20.0,
        address_line_1="123 Main St",
        address_line_2="Apt 4",
        city="City",
        postal_code="12345",
        country="Country",
        is_default=True,
        created_at=None,
    )

    with patch('data_access.repository.DatabaseRepository.fetch', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = address_data

        with pytest.raises(BaseError) as exc_info:
            await AddressDomain.load("user_id_123", "address_id_123")

        assert exc_info.value.error_code == ErrorCodes.ADDRESS_PERMISSION_DENIED_ERROR
        mock_fetch.assert_called_once_with(AddressDTO, query={"id": "address_id_123"}, one_or_none=True)


@pytest.mark.asyncio
async def test_create_address_success():
    address_data = AddressDTO(
        address_id="address_id_123",
        user_id="user_id_123",
        latitude=10.0,
        longitude=20.0,
        address_line_1="123 Main St",
        address_line_2="Apt 4",
        city="City",
        postal_code="12345",
        country="Country",
        is_default=True,
        created_at=None,
    )

    with patch('data_access.repository.DatabaseRepository.insert', new_callable=AsyncMock) as mock_insert:
        mock_insert.return_value = address_data

        address = await AddressDomain.create_address(
            user_id="user_id_123",
            latitude=10.0,
            longitude=20.0,
            address_line_1="123 Main St",
            address_line_2="Apt 4",
            city="City",
            postal_code="12345",
            country="Country",
            is_default=True,
        )

        assert address is not None
        assert address.address_id == "address_id_123"
        assert address.user_id == "user_id_123"
        mock_insert.assert_called_once()


@pytest.mark.asyncio
async def test_delete_address_success():
    with patch('data_access.repository.DatabaseRepository.delete', new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = True

        address = AddressDomain(
            address_id="address_id_123",
            user_id="user_id_123",
            latitude=10.0,
            longitude=20.0,
            address_line_1="123 Main St",
            address_line_2="Apt 4",
            city="City",
            postal_code="12345",
            country="Country",
            is_default=True,
            created_at=None,
        )

        result = await address.delete()
        assert result is True
        mock_delete.assert_called_once_with(AddressDTO, query={"id": "address_id_123"})


@pytest.mark.asyncio
async def test_update_information_success():
    updated_address_data = AddressDTO(
        address_id="address_id_123",
        user_id="user_id_123",
        latitude=15.0,
        longitude=25.0,
        address_line_1="456 Elm St",
        address_line_2="Suite 10",
        city="New City",
        postal_code="54321",
        country="New Country",
        is_default=True,
        created_at=None,
    )

    with patch('data_access.repository.DatabaseRepository.update', new_callable=AsyncMock) as mock_update:
        mock_update.return_value = updated_address_data

        address = AddressDomain(
            address_id="address_id_123",
            user_id="user_id_123",
            latitude=10.0,
            longitude=20.0,
            address_line_1="123 Main St",
            address_line_2="Apt 4",
            city="City",
            postal_code="12345",
            country="Country",
            is_default=True,
            created_at=None,
        )

        result = await address.update_information(
            latitude=15.0,
            longitude=25.0,
            address_line_1="456 Elm St",
            address_line_2="Suite 10",
            city="New City",
            postal_code="54321",
            country="New Country",
        )

        assert result['latitude'] == 15.0
        assert result['longitude'] == 25.0
        assert result['address_line_1'] == "456 Elm St"
        mock_update.assert_called_once()

