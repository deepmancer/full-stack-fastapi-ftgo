import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from domain.assets import VehicleDomain
from domain.user import User
from ftgo_utils.errors import ErrorCodes
from domain.driver import Driver


@pytest.fixture
def user_data():
    return {
        'user_id': '123',
        'role': 'driver',
        'first_name': 'John',
        'last_name': 'Doe',
        'phone_number': '1234567890',
        'hashed_password': 'hashedpassword',
    }


@pytest.fixture
def driver(user_data):
    return Driver(**user_data)


@pytest.mark.asyncio
async def test_load_private_attributes(driver):
    with patch('domain.assets.VehicleDomain.load_driver_vehicle', new_callable=AsyncMock) as mock_load_vehicle:
        mock_load_vehicle.return_value = MagicMock()
        await driver.load_private_attributes()
        assert driver.vehicle is not None
        mock_load_vehicle.assert_awaited_once_with(driver_id=driver.user_id, raise_error_on_missing=False)


@pytest.mark.asyncio
async def test_get_vehicle_info(driver):
    with patch.object(driver, 'vehicle', new=MagicMock()) as mock_vehicle:
        mock_vehicle.get_info.return_value = {'info': 'vehicle_info'}
        result = await driver.get_vehicle_info()
        assert result == {'info': 'vehicle_info'}


@pytest.mark.asyncio
async def test_get_vehicle_info_no_vehicle(driver):
    result = await driver.get_vehicle_info()
    assert result == {}


@pytest.mark.asyncio
async def test_register_vehicle(driver):
    with patch('domain.assets.VehicleDomain.register_vehicle', new_callable=AsyncMock) as mock_register_vehicle:
        mock_vehicle = MagicMock()
        mock_vehicle.get_info.return_value = {'info': 'vehicle_info'}
        mock_register_vehicle.return_value = mock_vehicle
        result = await driver.register_vehicle('plate123', 'license123')
        assert driver.vehicle == mock_vehicle
        assert result == {'info': 'vehicle_info'}
        mock_register_vehicle.assert_awaited_once_with(driver_id=driver.user_id, plate_number='plate123', license_number='license123')


@pytest.mark.asyncio
async def test_delete_vehicle(driver):
    with patch.object(driver, 'vehicle', new=MagicMock()) as mock_vehicle:
        mock_vehicle.delete = AsyncMock()
        result = await driver.delete_vehicle()
        assert result is True
        assert driver.vehicle is None
        mock_vehicle.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_vehicle_no_vehicle(driver):
    result = await driver.delete_vehicle()
    assert result is False
