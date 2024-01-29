import faker
from src.http_client import HttpClient
from .utils import generate_customer, generate_post, retry, HttpMethodsEnum
from typing import Union, Any, Optional


class Service(HttpClient):

    def __init__(
            self, 
            host: str, 
            port: str,
            max_attempts:Optional[int]=3, 
            delay: Optional[int]=1
        ) -> None:
        self.base_url = f'http://{host}:{port}'
        self.max_attempts = max_attempts
        self.delay = delay
        self.default_headers = {'Content-Type': 'application/json'}

    @retry
    def register_new_customer(self):
        url = f"{self.base_url}/auth/signup"
        data = generate_customer()
        response = self.create_http_request(
            url=url,
            method=HttpMethodsEnum.post,
            json=data,
            headers=self.default_headers
        )
        if response.status_code == 201:
            return response
        return None

    @retry    
    def create_post(self, token) -> Union[dict[str, str], None]:
        url = f"{self.base_url}/post/create"
        headers = self.default_headers.copy()
        headers.update({"Authorization": f"Bearer {token}"})
        response = self.create_http_request(
            url=url,
            method=HttpMethodsEnum.post,
            headers=headers,
            json=generate_post()
        )
        if response.status_code == 201:
            return response
        return None
    
    @retry
    def like_post(self, post_id: int, token: str) -> Union[dict[str, str], None]:
        url = f"{self.base_url}/post/{post_id}/like"
        headers = self.default_headers.copy()
        headers.update({"Authorization": f"Bearer {token}"})
        response = self.create_http_request(
            url=url,
            method=HttpMethodsEnum.post,
            headers=headers
        )
        if response.status_code == 200:
            return response
        return None


    @retry
    def dislike_post(self, post_id: int, token: str) -> Union[dict[str, str], None]:
        url = f"{self.base_url}/post/{post_id}/dislike"
        response = self.create_http_request(
            url=url,
            method=HttpMethodsEnum.post,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        if response.status_code == 200:
            return response
        return None
