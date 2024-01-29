from api_client import ApiClient
import pytest

@pytest.mark.registration
class TestRegistration:

    client = ApiClient()

    def test_registration(self, user_data: dict) -> None:
        result = self.client.register_customer(user_data)
        assert result.is_ok()
        user: dict = result.get_value().json()
        expected_keys = ['message', 'refresh_token', 'access_token', 'user']
        received_keys = user.keys()
        assert all([
            item in expected_keys
            for item in received_keys
        ])
        assert user['message'] == 'User registered successfully'
        for key, value in user['user'].items():
            assert user_data[key] == value

    def test_without_required_fields(self, user_data: dict) -> None:
        del user_data['email']
        result = self.client.register_customer(user_data)
        assert result.is_error()
        error = result.get_error().json()
        assert error['error_message'] == 'Request validation error'
        errors_list = error['errors']
        assert len(errors_list) == 1
        assert errors_list[0] == {'field': 'email', 'error_description': 'Field required'}
    
    def test_invalid_email(self, user_data: dict) -> None:
        user_data['email'] = 'invalid_email'
        result = self.client.register_customer(user_data)
        assert result.is_error()
        error = result.get_error().json()
        assert error['error_message'] == 'Request validation error'
        errors_list = error['errors']
        assert len(errors_list) == 1
        assert errors_list[0]['field'] == 'email'
    
    def test_invalid_birthday(self, user_data: dict) -> None:
        user_data["birthday"] = "2019-01-25"
        result = self.client.register_customer(user_data)
        assert result.is_error()
        error = result.get_error().json()
        assert error['error_message'] == 'Request validation error'
        errors_list = error['errors']
        assert len(errors_list) == 1
        assert errors_list[0] == {'field': 'birthday', 'error_description': 'Value error, User must be at least 13 y.o.'}

        