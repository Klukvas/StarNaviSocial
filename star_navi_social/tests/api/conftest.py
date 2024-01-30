from uuid import uuid4

import pytest


@pytest.fixture
def user_data() -> dict:
    return {
        "firstname": "string",
        "lastname": "string",
        "email": f"{str(uuid4())}@example.com",
        "phoneNum": str(int(uuid4())),
        "birthday": "2010-01-25",
        "username": str(uuid4()),
        "password": "asfnksadfnkasf",
        "password_confirmation": "asfnksadfnkasf",
        "subscribed_for_newsletter": False,
    }
