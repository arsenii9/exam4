from Cinescope.custom_requester.custom_requester import CustomRequester
from Cinescope.constants import MOVIE_BASE_URL, MOVIES_ENDPOINT

class MoviesApi(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIE_BASE_URL)

    def get_movies_list(self, params = None, expected_status = 200):
        return self.send_request(method="GET",
                                 endpoint=MOVIES_ENDPOINT,
                                 params=params,
                                 expected_status=expected_status)



    def post_movie(self, data,  expected_status = 201):
        return self.send_request(method="POST",
                                 endpoint=MOVIES_ENDPOINT,
                                 data=data,
                                 expected_status=expected_status)


    def get_movie(self, movie_id, expected_status = 200):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status = 200):
        return self.send_request(
            method="DELETE",
            endpoint = f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status = expected_status
        )

    def patch_movie(self, movie_id, data, expected_status = 200):
        return self.send_request(
            method="PATCH",
            endpoint = f"{MOVIES_ENDPOINT}/{movie_id}",
            data=data,
            expected_status = expected_status
        )


