import os
from fastapi import FastAPI
from application.schema import (
    RegisterRequest, RegisterResponse,
    AuthenticatePhoneNumberRequest, AuthenticatePhoneNumberResponse,
    LoginRequest, LoginResponse,
    GetUserInfoRequest, GetUserInfoResponse,
    AddAddressRequest, AddressResponse,
    ModifyAddressRequest,
    DeleteAddressRequest,
    SetPreferredAddressRequest,
    DeleteAccountRequest, DeleteAccountResponse,
    DeleteAllAddressesRequest, DeleteAllAddressesResponse
)
from domain.user import UserDomain


app = FastAPI(title=os.getenv("SERVICE_CONTAINER_NAME"), debug=True)

@app.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest):
    return await events["register"](request)

@app.post("/authenticate-phone-number", response_model=AuthenticatePhoneNumberResponse)
async def authenticate_phone_number(request: AuthenticatePhoneNumberRequest):
    return await events["authenticate_phone_number"](request)

@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    return await events["login"](request)

@app.get("/user-info", response_model=GetUserInfoResponse)
async def get_user_info(user_id: str):
    request = GetUserInfoRequest(user_id=user_id)
    return await events["get_user_info"](request)

@app.post("/add-address", response_model=AddressResponse)
async def add_address(request: AddAddressRequest):
    return await events["add_address"](request)

@app.post("/modify-address", response_model=AddressResponse)
async def modify_address(request: ModifyAddressRequest):
    return await events["modify_address"](request)

@app.delete("/delete-address", response_model=AddressResponse)
async def delete_address(address_id: str):
    request = DeleteAddressRequest(address_id=address_id)
    return await events["delete_address"](request)

@app.post("/set-preferred-address", response_model=AddressResponse)
async def set_preferred_address(request: SetPreferredAddressRequest):
    return await events["set_preferred_address"](request)
