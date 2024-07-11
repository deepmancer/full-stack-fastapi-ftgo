import os
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application import get_logger
from application.schema import (
    RegisterRestaurantRequest, RegisterRestaurantResponse,
    AddMenuItemRequest, AddMenuItemResponse,
    UpdateMenuItemRequest, UpdateMenuItemResponse,
    DeleteMenuItemRequest, DeleteMenuItemResponse,
    GetMenuRequest, GetMenuResponse,
    ReceiveOrderRequest, ReceiveOrderResponse,
    UpdateOrderStatusRequest, UpdateOrderStatusResponse,
    GetOrdersRequest, GetOrdersResponse,
    GetRestaurantInfoRequest, GetRestaurantInfoResponse,
    UpdateRestaurantInfoRequest, UpdateRestaurantInfoResponse,
)


from domain.restaurant import RestaurantDomain

router = APIRouter(prefix="/restaurant", tags=["restaurant"])

@router.post("/register", response_model=RegisterRestaurantResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRestaurantRequest):
    try:
        restaurant_id = await RestaurantDomain.register(
            name=request.name,
            address=request.address,
            phone_number=request.phone_number,
            email=request.email,
            owner_id=request.owner_id,
        )
        return RegisterRestaurantResponse(restaurant_id=restaurant_id)
    except Exception as e:
        get_logger().error(f"Error occurred while registering restaurant: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/menu/item", response_model=AddMenuItemResponse)
async def add_menu_item(request: AddMenuItemRequest):
    try:
        item_id = await RestaurantDomain.add_menu_item(
            restaurant_id=request.restaurant_id,
            name=request.name,
            description=request.description,
            price=request.price,
            category=request.category,
        )
        return AddMenuItemResponse(item_id=item_id)
    except Exception as e:
        get_logger().error(f"Error occurred while adding menu item: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.put("/menu/item", response_model=UpdateMenuItemResponse)
async def update_menu_item(request: UpdateMenuItemRequest):
    try:
        await RestaurantDomain.update_menu_item(
            item_id=request.item_id,
            name=request.name,
            description=request.description,
            price=request.price,
            category=request.category,
        )
        return UpdateMenuItemResponse(item_id=request.item_id)
    except Exception as e:
        get_logger().error(f"Error occurred while updating menu item: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.delete("/menu/item", response_model=DeleteMenuItemResponse)
async def delete_menu_item(request: DeleteMenuItemRequest):
    try:
        await RestaurantDomain.delete_menu_item(item_id=request.item_id)
        return DeleteMenuItemResponse(item_id=request.item_id)
    except Exception as e:
        get_logger().error(f"Error occurred while deleting menu item: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.get("/menu", response_model=GetMenuResponse)
async def get_menu(request: GetMenuRequest):
    try:
        menu = await RestaurantDomain.get_menu(restaurant_id=request.restaurant_id)
        return GetMenuResponse(menu=menu)
    except Exception as e:
        get_logger().error(f"Error occurred while getting menu: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/order", response_model=ReceiveOrderResponse)
async def receive_order(request: ReceiveOrderRequest):
    try:
        order_id = await RestaurantDomain.receive_order(
            restaurant_id=request.restaurant_id,
            items=request.items,
            customer_id=request.customer_id,
            delivery_address=request.delivery_address,
        )
        return ReceiveOrderResponse(order_id=order_id)
    except Exception as e:
        get_logger().error(f"Error occurred while receiving order: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.put("/order/status", response_model=UpdateOrderStatusResponse)
async def update_order_status(request: UpdateOrderStatusRequest):
    try:
        await RestaurantDomain.update_order_status(
            order_id=request.order_id,
            status=request.status,
        )
        return UpdateOrderStatusResponse(order_id=request.order_id)
    except Exception as e:
        get_logger().error(f"Error occurred while updating order status: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.get("/orders", response_model=GetOrdersResponse)
async def get_orders(request: GetOrdersRequest):
    try:
        orders = await RestaurantDomain.get_orders(restaurant_id=request.restaurant_id)
        return GetOrdersResponse(orders=orders)
    except Exception as e:
        get_logger().error(f"Error occurred while getting orders: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.get("/info", response_model=GetRestaurantInfoResponse)
async def get_info(request: GetRestaurantInfoRequest):
    try:
        info = await RestaurantDomain.get_info(restaurant_id=request.restaurant_id)
        return GetRestaurantInfoResponse(info=info)
    except Exception as e:
        get_logger().error(f"Error occurred while getting restaurant info: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.put("/info", response_model=UpdateRestaurantInfoResponse)
async def update_info(request: UpdateRestaurantInfoRequest):
    try:
        await RestaurantDomain.update_info(
            restaurant_id=request.restaurant_id,
            name=request.name,
            address=request.address,
            phone_number=request.phone_number,
            email=request.email,
        )
        return UpdateRestaurantInfoResponse(restaurant_id=request.restaurant_id)
    except Exception as e:
        get_logger().error(f"Error occurred while updating restaurant info: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
