import uuid
import httpx
from fastapi import HTTPException, status
from typing import Dict
from utils.dummy import generate_user, roles

API_BASE_URL = "http://localhost:8000/api/v1"

class UserManager:
    def __init__(self):
        self.users = {}

    async def add_customer(self, role: str = "customer") -> Dict:
        if role not in roles:
            raise ValueError(f"Invalid role: {role}. Must be one of {roles}.")

        user_data = generate_user(role)

        async with httpx.AsyncClient() as client:
            # Step 1: Register the user
            register_response = await client.post(f"{API_BASE_URL}/auth/register", json=user_data)
            if register_response.status_code != 201:
                raise HTTPException(status_code=register_response.status_code, detail=register_response.json().get("detail", "Registration failed"))
            
            user_id = register_response.json().get("user_id")
            auth_code = register_response.json().get("auth_code")

            # Step 2: Verify the user
            verify_data = {"user_id": user_id, "auth_code": auth_code}
            verify_response = await client.post(f"{API_BASE_URL}/auth/verify", json=verify_data)
            if verify_response.status_code != 200:
                raise HTTPException(status_code=verify_response.status_code, detail=verify_response.json().get("detail", "Verification failed"))

            # Step 3: Log in the user
            login_data = {
                "phone_number": user_data["phone_number"],
                "role": user_data["role"],
                "password": user_data["password"],
            }
            login_response = await client.post(f"{API_BASE_URL}/auth/login", json=login_data)
            if login_response.status_code != 200:
                raise HTTPException(status_code=login_response.status_code, detail=login_response.json().get("detail", "Login failed"))
            
            login_response_data = login_response.json()
            token = login_response_data.get("token")

            # Save the token and user data in the UserManager's user dictionary
            self.users[user_id] = {
                **user_data,
                "token": token,
            }

            return self.users[user_id]

    def get_user(self, user_id: str) -> Dict:
        if user_id not in self.users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return self.users[user_id]

    async def add_address(self, user_id: str, address_data: Dict) -> Dict:
        if user_id not in self.users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        token = self.users[user_id]["token"]

        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(f"{API_BASE_URL}/address/add", json=address_data, headers=headers)
            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Address addition failed"))
            self.users[user_id]["addresses"].append(address_data)
            return self.users[user_id]

user_manager = UserManager()
