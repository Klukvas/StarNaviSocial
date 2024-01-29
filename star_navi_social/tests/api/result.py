from typing import Any, Union


class Result:
    def __init__(
        self,
        failed_response: Union[dict, None] = None,
        success_response: Union[dict, None] = None,
    ) -> None:
        self.failed_response = failed_response
        self.success_response = success_response
        self.json_response = None

    def is_ok(self) -> bool:
        return False

    def is_error(self) -> bool:
        return False

    def get_value_or(self, default: Any = None) -> Any:
        if self.success_response:
            return self.success_response
        return default

    def get_error_or(self, default: Any = None) -> Any:
        if self.failed_response:
            return self.failed_response
        return default

    def repr(self) -> str:
        return str(self.json_response)


class Ok(Result):
    def __init__(self, response: dict) -> None:
        super().__init__(success_response=response)
        self.json_response = response

    def is_ok(self):
        return True

    def get_value(self) -> Union[dict, list]:
        return self.json_response


class Error(Result):
    def __init__(self, response: dict) -> None:
        super().__init__(failed_response=response)
        self.json_response = response

    def is_error(self):
        return True

    def get_error(self) -> dict:
        return self.json_response