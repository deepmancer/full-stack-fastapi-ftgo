from typing import Dict, Any, Optional
from domain.menu import MenuDomain
from domain.restaurant import RestaurantDomain

class MenuService:
    """
    Service class for managing menu items.
    """

    @staticmethod
    async def add_item(
        restaurant_id: str,
        name: str,
        price: float,
        description: str,
    ) -> Dict[str, Any]:
        """
        Adds a new menu item.

        :param restaurant_id: ID of the Restaurant.
        :param name: Name of the menu item.
        :param price: Price of the menu item.
        :param description: Description of the menu item.
        :return: Dictionary containing the menu item ID.
        """
        menu_item = await MenuDomain.add_item(restaurant_id=restaurant_id, name=name, price=price,
                                              description=description)
        return {
            "item_id": menu_item.item_id
        }

    @staticmethod
    async def update_item(
        item_id: str,
        name: Optional[str] = None,
        price: Optional[float] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Updates a menu item's information.

        :param item_id: ID of the menu item.
        :param name: New name of the menu item.
        :param price: New price of the menu item.
        :param description: New description of the menu item.
        :return: Dictionary containing updated menu item information.
        """
        return await MenuDomain.update_item(item_id=item_id, name=name, price=price,
                                            description=description)

    @staticmethod
    async def delete_item(item_id: str) -> Dict[str, str]:
        """
        Deletes a menu item.

        :param item_id: ID of the menu item.
        :return: Dictionary containing the ID of the deleted item.
        """
        await MenuDomain.delete_item(item_id=item_id)
        return {
            "item_id": item_id,
        }


    @staticmethod
    async def get_item_info(item_id: str) -> Dict[str, Any]:
        """
        Retrieves menu item information.

        :param item_id: ID of the menu item.
        :return: Dictionary containing menu item information.
        """
        menu_item = await MenuDomain.load(item_id=item_id)
        if not menu_item:
            return {"error": "Item not found"}
        return menu_item.to_dict()

    @staticmethod
    async def get_all_menu_item(restaurant_id: str) -> Dict[str, Any]:
        """
        Retrieves all menu item associated with the restaurant's account.

        :param restaurant_id: ID of the user.
        :return: Dictionary containing status and a list of menu item.
        """
        restaurant = await RestaurantDomain.load(restaurant_id)
        menu = await restaurant.get_all_menu_item_info()
        return {
            "menu": menu,
        }
