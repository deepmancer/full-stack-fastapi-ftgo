# import os
# from fastapi import APIRouter, status, HTTPException, Request
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# from application import get_logger
# from application.schemas.routes.registration import (
#     LogoutResponse, GetUserInfoResponse, DeleteProfileResponse,
# )
# from application.schemas.user import UserSchema
# from ftgo_utils.enums import ResponseStatus
# from services.user import UserService

# router = APIRouter(prefix='/profile', tags=["user_profile"])
# logger = get_logger()

# @router.post("/logout", response_model=LogoutResponse)
# async def logout(request: Request):
#     try:
#         user: UserSchema = request.state.user
#         response = await UserService.logout(data={"user_id": user.user_id})
#         if response.get('status') == ResponseStatus.ERROR.value:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, 
#                 detail=response.get('error_message', 'Logout failed')
#             )
#         return LogoutResponse(user_id=user.user_id)
#     except Exception as e:
#         logger.error(f"Error occurred while logging the user out: {e}", exc_info=True)
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             content=jsonable_encoder({"detail": str(e)})
#         )

# @router.get("/user_info", response_model=GetUserInfoResponse)
# async def get_info(request: Request):
#     try:
#         user: UserSchema = request.state.user
#         response = await UserService.get_profile_info(data={"user_id": user.user_id})
#         if response.pop('status', ResponseStatus.ERROR.value) == ResponseStatus.ERROR.value:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, 
#                 detail=response.get('error_message', 'Get user information failed')
#             )
#         return GetUserInfoResponse(
#             first_name=response.get("first_name"),
#             last_name=response.get("last_name"),
#             phone_number=response.get("phone_number"),
#             national_id=response.get("national_id"),
#         )
#     except Exception as e:
#         logger.error(f"Error occurred while getting the user info: {e}", exc_info=True)
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             content=jsonable_encoder({"detail": str(e)})
#         )

# @router.delete("/delete", response_model=DeleteProfileResponse)
# async def delete_account(request: Request):
#     try:
#         user: UserSchema = request.state.user
#         response = await UserService.delete_account(data={"user_id": user.user_id})
#         if response.get('status') == ResponseStatus.ERROR.value:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, 
#                 detail=response.get('error_message', 'Account deletion failed')
#             )
#         return DeleteProfileResponse(success=True)
#     except Exception as e:
#         logger.error(f"Error occurred while deleting the account: {e}", exc_info=True)
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             content=jsonable_encoder({"detail": str(e)})
#         )
