import pytest
import allure
from Cinescope.conftest import common_user
from Cinescope.utils.data_generator import DataGenerator

class TestMoviesAPINegative:
    pytestmark = pytest.mark.negative

    @allure.title("Получение фильма по неверному id")
    def test_get_movie_by_invalid_id(self, common_user):
        common_user.api.movies_api.get_movie(movie_id=999999, expected_status=404)

    @allure.title("Создание фильма с невалидными данными")
    @pytest.mark.slow
    def test_create_movie_with_invalid_data(self, super_admin_user):
        data = {
            "name": "",
            "imageUrl": "invalid_url",
            "price": "abc",
            "description": "",
            "location": "INVALID",
            "published": "not_bool",
            "genreId": "wrong"
        }

        super_admin_user.api.movies_api.post_movie(data=data, expected_status=400)

    @allure.title("Обновление фильма по неверному id")
    def test_patch_movie_with_invalid_id(self, super_admin_user):
        data = {
            "name": "abc"
        }
        super_admin_user.api.movies_api.patch_movie(movie_id=999999, data=data, expected_status=404)

    @allure.title("Удаление фильма по неверному id")
    def test_delete_movie_by_invalid_id(self, super_admin_user):
        super_admin_user.api.movies_api.delete_movie(movie_id=99999999, expected_status=404)

    @allure.title("Создание фильма с недостаточными правами")
    def test_create_movie_by_common_user(self, common_user):
        with allure.step("Сгенерировать payload для создания фильма"):
            data = DataGenerator.generate_movie_payload()

        with allure.step("Отправить POST-запрос на создание фильма от пользователя без прав"):
            common_user.api.movies_api.post_movie(data=data, expected_status=403)

