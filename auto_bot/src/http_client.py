from requests import request, Response
from .utils import HttpMethodsEnum
from typing import Optional

class HttpClient:

    def create_http_request(
            self, 
            url: str, 
            method: HttpMethodsEnum,
            json: Optional[dict] = None,
            headers: Optional[dict] = None
    ) -> Response:
        result = request(
            method=method,
            url=url,
            json=json,
            headers=headers
        )
        return result