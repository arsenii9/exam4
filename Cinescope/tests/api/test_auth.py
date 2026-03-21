
class TestAuthAPI:
    def test_register_user(self, test_user, api_manager):
        response = api_manager.auth_api.register_user(test_user)

        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_login_user(self, registered_user, api_manager):
        response = api_manager.auth_api.login_user(registered_user["data"])

        response_data = response.json()

        assert "accessToken" in response_data
        assert "email" in response_data["user"], "В ответе нет email"
        assert response_data["user"]["email"] == registered_user["data"]["email"], "Email не совпадает"

    def test_negative_wrong_pass(self, test_user, api_manager):
        wrong_user = test_user.copy()
        wrong_user["password"] = "qwerty"

        response = api_manager.auth_api.login_user(wrong_user, expected_status=401)
        response_data = response.json()

        assert "error" in response_data

    def test_negative_wrong_email(self, test_user, api_manager):
        wrong_user = test_user.copy()
        wrong_user["email"] = "qwerty"

        response = api_manager.auth_api.login_user(wrong_user, expected_status=401)
        response_data = response.json()

        assert "error" in response_data

    def test_negative_void_body(self, api_manager):
        response = api_manager.auth_api.login_user(None, expected_status=401)
        response_data = response.json()

        assert "error" in response_data