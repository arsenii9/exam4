from Cinescope.utils.data_generator import DataGenerator

class TestMoviesAPI:

        #Positive

    def test_get_list(self, api_manager):
        response = api_manager.movies_api.get_movies_list(expected_status=200)
        assert response.json() is not None
        assert isinstance(response.json(), dict)

    def test_get_filter_by_price(self, api_manager):
        params  = {
            "minPrice": 3,
            "maxPrice": 500
        }
        response = api_manager.movies_api.get_movies_list(params=params, expected_status=200)
        data = response.json()
        assert data is not None
        assert isinstance(data, dict)
        for movie in data["movies"]:
            assert movie["price"] >= 3 and movie["price"] <= 500

    def test_create_movie(self, api_admin):
        data = DataGenerator.generate_movie_payload()
        response = api_admin.movies_api.post_movie(data=data, expected_status=201)
        response_data = response.json()
        assert response_data is not None
        assert isinstance(response_data, dict)
        assert data["name"] == response_data["name"]

    def test_get_movie_by_id(self, api_manager, created_movie):
            response = api_manager.movies_api.get_movie(movie_id=created_movie["id"], expected_status=200)
            response_data = response.json()
            assert created_movie["id"] == response_data["id"]

    def test_delete_movie_by_id(self, api_admin):
        data = DataGenerator.generate_movie_payload()
        movie = api_admin.movies_api.post_movie(data=data, expected_status=201).json()

        api_admin.movies_api.get_movie(movie_id=movie["id"], expected_status=200)
        api_admin.movies_api.delete_movie(movie_id=movie["id"], expected_status=200)
        api_admin.movies_api.get_movie(movie_id=movie["id"], expected_status=404)



    def test_patch_movie(self, api_admin, created_movie):
        data = {
            "name": "abc"
        }
        response = api_admin.movies_api.patch_movie(movie_id=created_movie["id"], data=data, expected_status=200)
        response_data = response.json()
        assert created_movie["data"]["name"] != response_data["name"]
        assert created_movie["data"]["imageUrl"] == response_data["imageUrl"]
        assert response_data["name"] == data["name"]


        #Negative


    def test_get_movie_by_invalid_id(self, api_manager):
        api_manager.movies_api.get_movie(movie_id=999999, expected_status=404)

    def test_create_movie_with_invalid_data(self, api_admin):
        data = {
            "name": "",
            "imageUrl": "invalid_url",
            "price": "abc",
            "description": "",
            "location": "INVALID",
            "published": "not_bool",
            "genreId": "wrong"
        }

        api_admin.movies_api.post_movie(data=data, expected_status=400)

    def test_patch_movie_with_invalid_id(self, api_admin):
        data = {
            "name": "abc"
        }
        api_admin.movies_api.patch_movie(movie_id=999999, data=data, expected_status=404)

    def test_delete_movie_by_invalid_id(self, api_admin):
        api_admin.movies_api.delete_movie(movie_id=99999999, expected_status=404)

