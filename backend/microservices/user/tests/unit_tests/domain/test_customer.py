import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from domain.customer import Customer


@pytest.fixture
def user_data():
    return {
        'user_id': '123',
        'role': 'customer',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'phone_number': '9876543210',
        'hashed_password': 'hashedpassword',
    }


@pytest.fixture
def customer(user_data):
    return Customer(**user_data)


@pytest.mark.asyncio
async def test_load_private_attributes(customer):
    with patch('domain.assets.AddressDomain.load_user_addresses', new_callable=AsyncMock) as mock_load_addresses:
        mock_load_addresses.return_value = [MagicMock()]
        await customer.load_private_attributes()
        assert len(customer.addresses) == 1
        mock_load_addresses.assert_awaited_once_with(customer.user_id, raise_error_on_missing=False)


def test_get_addresses_info(customer):
    mock_address = MagicMock()
    mock_address.get_info.return_value = {'info': 'address_info'}
    customer.addresses = [mock_address]
    result = customer.get_addresses_info()
    assert result == [{'info': 'address_info'}]


@pytest.mark.asyncio
async def test_get_address_info(customer):
    mock_address = MagicMock()
    mock_address.get_info.return_value = {'info': 'address_info'}
    customer.addresses = [mock_address]

    with patch.object(customer, 'get_address', new_callable=AsyncMock) as mock_get_address:
        mock_get_address.return_value = mock_address
        result = await customer.get_address_info('address_id')
        assert result == {'info': 'address_info'}
        mock_get_address.assert_awaited_once_with('address_id')


@pytest.mark.asyncio
async def test_get_address(customer):
    mock_address = MagicMock()
    mock_address.address_id = 'address_id'
    customer.addresses = [mock_address]
    result = await customer.get_address('address_id')
    assert result == mock_address



@pytest.mark.asyncio
async def test_add_address(customer):
    mock_address = MagicMock()
    mock_address.get_info.return_value = {'info': 'address_info'}

    with patch('domain.assets.AddressDomain.create_address', new_callable=AsyncMock) as mock_create_address:
        mock_create_address.return_value = mock_address
        result = await customer.add_address(
            latitude=1.0,
            longitude=1.0,
            address_line_1='123 Main St',
            address_line_2='Apt 4B',
            city='Metropolis',
            postal_code='12345',
            country='Country'
        )
        assert result == {'info': 'address_info'}
        assert mock_address in customer.addresses
        mock_create_address.assert_awaited_once_with(
            user_id=customer.user_id,
            latitude=1.0,
            longitude=1.0,
            address_line_1='123 Main St',
            address_line_2='Apt 4B',
            city='Metropolis',
            is_default=True,
            postal_code='12345',
            country='Country'
        )




@pytest.mark.asyncio
async def test_delete_address(customer):
    mock_address = MagicMock()
    mock_address.address_id = 'address_id'
    customer.addresses = [mock_address]

    with patch.object(customer, 'get_address', new_callable=AsyncMock) as mock_get_address:
        mock_get_address.return_value = mock_address
        mock_address.delete = AsyncMock()
        result = await customer.delete_address('address_id')
        assert result is True
        assert not any(addr.address_id == 'address_id' for addr in customer.addresses)
        mock_get_address.assert_awaited_once_with('address_id')
        mock_address.delete.assert_awaited_once()

