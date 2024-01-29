from typing import Any, Union


class ExceptionError(Exception):
    "Common error exception"

    def __init__(
            self, 
            message: str, 
            status_code: int,
            fields: Union[dict[str, Any], None] = None
        ) -> None:
        self.message = message
        self.status_code = status_code
        self.fields = fields
        