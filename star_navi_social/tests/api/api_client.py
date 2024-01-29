from main import app
from fastapi.testclient import TestClient
from typing import Union, Optional
from uuid import uuid4
from result import Ok, Error

class ApiClient:
    
    def __init__(self) -> None:
        self.client = TestClient(app)
        self.default_headers = {'Content-Type': 'application/json'}
    
    def _generate_user_data(self) -> dict:
        return {
            "firstname": "string",
            "lastname": "string",
            "email": f"{str(uuid4())}@example.com",
            "phoneNum": str(int(uuid4())),
            "birthday": "2010-01-25",
            "username": str(uuid4()),
            "password": "asfnksadfnkasf",
            "password_confirmation": "asfnksadfnkasf",
            "subscribed_for_newsletter": False
        }

    def register_customer(self, user_data: Optional[dict]=None) -> Union[Ok, Error]:
        response = self.client.post(
            '/auth/signup',
            json=user_data if user_data else self._generate_user_data(),
            headers=self.default_headers
        )
        if response.status_code != 201:
            return Error(response)
        return Ok(response)
    
    def create_post(self, token: str) -> Union[Ok, Error]:
        headers = {"Authorization": f"Bearer {token}"}
        headers.update(self.default_headers)
        response = self.client.post(
            '/auth/signup',
            json={
                "title": "string",
                "description": "string"
            },
            headers=headers
        )

        if response.status_code != 201:
            return Error(response)
        return Ok(response)
    
    def like_post(self, post_id: int, token: str) -> Union[Ok, Error]:
        headers = {"Authorization": f"Bearer {token}"}
        headers.update(self.default_headers)
        response = self.client.post(
            f'/post/{post_id}/like',
            headers=headers
        )

        if response.status_code != 200:
            return Error(response)
        return Ok(response)
    