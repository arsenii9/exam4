import pytest
import allure
from Cinescope.conftest import db_session
from Cinescope.db_models.movie import MovieDBModel
from Cinescope.utils.data_generator import DataGenerator
from Cinescope.models.movie_model import MoviesResponse, Movie

class TestMoviesAPIPositive:
    pytestmark = pytest.mark.positive

    @allure.title("Получение списка фильмов")
    def test_get_list(self, common_user):
        response = common_user.api.movies_api.get_movies_list(expected_status=200)
        data = MoviesResponse(**response.json())
        assert data is not None
        assert isinstance(data, MoviesResponse)

    @allure.title("Получение списка фильмов с фильтром по цене")
    def test_get_filter_by_price(self, common_user):
        params  = {
            "minPrice": 3,
            "maxPrice": 500
        }
        response = common_user.api.movies_api.get_movies_list(params=params, expected_status=200)
        data = MoviesResponse(**response.json())
        assert data is not None
        assert isinstance(data, MoviesResponse)
        for movie in data.movies:
            assert movie.price >= 3 and movie.price <= 500

    @allure.title("Создание фильма")
    def test_create_movie(self, super_admin_user):
        data = DataGenerator.generate_movie_payload()
        response = super_admin_user.api.movies_api.post_movie(data=data, expected_status=201)
        movie_data = Movie(**response.json())
        assert movie_data is not None
        assert isinstance(movie_data, Movie)
        assert data["name"] == movie_data.name

    @allure.title("Получение фильма по id")
    @pytest.mark.slow
    def test_get_movie_by_id(self, common_user, created_movie):
            response = common_user.api.movies_api.get_movie(movie_id=created_movie["id"], expected_status=200)
            movie_data = Movie(**response.json())
            assert created_movie["id"] == movie_data.id

    @allure.title("Удаление фильма")
    def test_delete_movie_by_id(self, super_admin_user):
        data = DataGenerator.generate_movie_payload()
        movie = super_admin_user.api.movies_api.post_movie(data=data, expected_status=201).json()

        super_admin_user.api.movies_api.get_movie(movie_id=movie["id"], expected_status=200)
        super_admin_user.api.movies_api.delete_movie(movie_id=movie["id"], expected_status=200)
        super_admin_user.api.movies_api.get_movie(movie_id=movie["id"], expected_status=404)

    @allure.title("Обновление фильма")
    @pytest.mark.slow
    def test_patch_movie(self, super_admin_user, created_movie):
        data = {
            "name": "abc"
        }
        response = super_admin_user.api.movies_api.patch_movie(movie_id=created_movie["id"], data=data, expected_status=200)
        movie_data = Movie(**response.json())
        assert created_movie["data"]["name"] != movie_data.name
        assert created_movie["data"]["imageUrl"] == movie_data.imageUrl
        assert data["name"] == movie_data.name

    @allure.title("Получение списка фильмов с параметризированным фильтром")
    @pytest.mark.parametrize(
        "filter_type, params",
        [
            ("price", {"minPrice": 100, "maxPrice": 2000}),
            ("location", {"locations": ["MSK"]}),
            ("genre", {"genreId": 3}),
        ]
    )
    def test_movies_filters(self, common_user, filter_type, params):
        response = common_user.api.movies_api.get_movies_list(params=params, expected_status=200)
        movies_response = MoviesResponse(**response.json())

        for movie in movies_response.movies:
            if filter_type == "price":
                assert params["minPrice"] <= movie.price <= params["maxPrice"]

            elif filter_type == "location":
                assert movie.location in params["locations"]

            elif filter_type == "genre":
                assert movie.genreId == params["genreId"]

    @allure.title("Попытки удалить фильтр с разными ролями")
    @pytest.mark.slow
    @pytest.mark.parametrize(
        "user_fixture, expected_status",
        [
            ("super_admin_user", 200),
            ("admin_user", 403),
            ("common_user", 403),
        ]
    )
    def test_delete_movie_with_roles(self, request, user_fixture, expected_status, super_admin_user):
        data = DataGenerator.generate_movie_payload()
        movie = super_admin_user.api.movies_api.post_movie(data=data, expected_status=201).json()

        user = request.getfixturevalue(user_fixture)
        user.api.movies_api.delete_movie(movie_id=movie["id"], expected_status=expected_status)

        if expected_status == 200:
            super_admin_user.api.movies_api.get_movie(movie_id=movie["id"], expected_status=404)

    @allure.title("Создание фильма с проверкой в БД")
    def test_create_DB_check(self, super_admin_user, db_session):
        with allure.step("Сгенерировать payload для создания фильма"):
            data = DataGenerator.generate_movie_payload()

        with allure.step("Отправить POST-запрос на создание фильма"):
            response = super_admin_user.api.movies_api.post_movie(data=data, expected_status=201)

        with allure.step("Преобразовать ответ API в модель Movie"):
            movie_data = Movie(**response.json())

        with allure.step("Получить запись фильма из БД по id"):
            db_resp = db_session.query(MovieDBModel).filter_by(id=movie_data.id).one()

        with allure.step("Проверить соответствие данных в БД и отправленного payload"):
            assert db_resp.name == data["name"]
            assert db_resp.price == data["price"]
            assert db_resp.description == data["description"]
            assert db_resp.location == data["location"]
            assert db_resp.published == data["published"]
            assert db_resp.genre_id == data["genreId"]
