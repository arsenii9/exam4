import pytest
import requests

from Restful_Booker_API.custom_requester import CustomRequester

booking = {
    "firstname": "Vasiliy",
    "lastname": "Ivanov",
    "totalprice": 150,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2025-01-01",
        "checkout": "2026-01-01"
    },
    "additionalneeds": "dinner"
}

baseurl = "https://restful-booker.herokuapp.com"
auth = ("admin", "password123")


@pytest.fixture
def session():
    return requests.Session()


@pytest.fixture
def requester(session):
    return CustomRequester(session, baseurl)


@pytest.fixture
def auth_requester(session):
    req = CustomRequester(session, baseurl)
    req.session.auth = auth
    req.session.headers.update(req.headers)
    return req


@pytest.fixture
def booking_id(requester):
    response = requester.send_request(
        "POST",
        "/booking",
        data=booking,
        expected_status=200
    )
    return response.json()["bookingid"]


class TestBook:

    def test_create(self, requester):
        response = requester.send_request(
            "POST",
            "/booking",
            data=booking,
            expected_status=200
        )
        assert response.status_code == 200

    def test_get(self, requester, booking_id):
        get_res = requester.send_request(
            "GET",
            f"/booking/{booking_id}",
            expected_status=200
        )

        assert get_res.status_code == 200
        assert booking == get_res.json()

    def test_delete(self, auth_requester, booking_id):
        d = auth_requester.send_request(
            "DELETE",
            f"/booking/{booking_id}",
            expected_status=201
        )

        assert d.status_code == 201

        check = auth_requester.send_request(
            "GET",
            f"/booking/{booking_id}",
            expected_status=404
        )
        assert check.status_code == 404

    def test_put(self, auth_requester, booking_id):
        updated_booking = {
            "firstname": "Alex",
            "lastname": "Petrov",
            "totalprice": 200,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2027-01-01",
                "checkout": "2027-12-31"
            },
            "additionalneeds": "breakfast"
        }

        response = auth_requester.send_request(
            "PUT",
            f"/booking/{booking_id}",
            data=updated_booking,
            expected_status=200
        )

        assert response.status_code == 200

        get_res = auth_requester.send_request(
            "GET",
            f"/booking/{booking_id}",
            expected_status=200
        )
        assert get_res.json() == updated_booking

    def test_patch(self, auth_requester, booking_id):
        patch_data = {
            "firstname": "Sergey"
        }

        get_be = auth_requester.send_request(
            "GET",
            f"/booking/{booking_id}",
            expected_status=200
        )
        before_data = get_be.json()

        response = auth_requester.send_request(
            "PATCH",
            f"/booking/{booking_id}",
            data=patch_data,
            expected_status=200
        )

        assert response.status_code == 200

        get_af = auth_requester.send_request(
            "GET",
            f"/booking/{booking_id}",
            expected_status=200
        )
        after_data = get_af.json()

        assert after_data["firstname"] == "Sergey"
        assert after_data["lastname"] == before_data["lastname"]