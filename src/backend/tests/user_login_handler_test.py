import pytest
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.dependency(depends=['user_registration'], scope='session')
@pytest.mark.order(1)
class UserLoginHandlerTest:

    _end_point: str = '/api/auth/login'

    @classmethod
    def test_logging_in_with_the_wrong_username_raises_exception(
        cls,
        user_credentials: dict[str, str],
        test_client: TestClient
    ) -> None:

        response: Response = cls._request_login(
            test_client=test_client,
            username='wrong_username',
            password=user_credentials['password']
        )
        assert response.status_code == 401

    @classmethod
    def test_logging_in_with_the_wrong_password_raises_exception(
        cls,
        user_credentials: dict[str, str],
        test_client: TestClient
    ) -> None:

        response: Response = cls._request_login(
            test_client=test_client,
            username=user_credentials['username'],
            password='wrong_password'
        )
        assert response.status_code == 401

    @classmethod
    def test_registered_user_is_logged_in(cls, user_credentials: dict[str, str], test_client: TestClient) -> None:

        response: Response = cls._request_login(
            test_client=test_client,
            username=user_credentials['username'],
            password=user_credentials['password']
        )
        assert response.status_code == 200

    @classmethod
    def _request_login(cls, test_client: TestClient, username: str, password: str) -> Response:

        return test_client.post(
            url=cls._end_point,
            data={
                'username': username,
                'password': password
            }
        )
