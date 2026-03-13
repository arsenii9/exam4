import pytest
import requests

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

baseurl = "https://restful-booker.herokuapp.com/"
auth = ("admin", "password123")


@pytest.fixture
def session():
    return requests.Session()


@pytest.fixture
def booking_id(session):
    response = session.post(baseurl + "/booking", json=booking)
    assert response.status_code in (200, 201)

    return response.json()["bookingid"]


class TestBook:

    def test_create(self, session):
        response = session.post(baseurl + "/booking", json=booking)
        assert response.status_code in (200, 201), "error"

    def test_get(self, session, booking_id):
        get_res = session.get(baseurl + "/booking/" + str(booking_id))

        assert get_res.status_code == 200
        assert booking == get_res.json()

    def test_delete(self, session, booking_id):
        d = session.delete(baseurl + "/booking/" + str(booking_id), auth=auth)

        assert d.status_code in (200, 201, 204)
        assert session.get(baseurl + "/booking/" + str(booking_id)).status_code == 404

    def test_put(self, session, booking_id):
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

        response = session.put(baseurl + "/booking/" + str(booking_id), json=updated_booking, auth=auth)

        assert response.status_code == 200
        assert session.get(baseurl + "/booking/" + str(booking_id)).json() == updated_booking

    def test_patch(self, session, booking_id):
        patch_data = {
            "firstname": "Sergey"
        }

        get_be = session.get(baseurl + "/booking/" + str(booking_id)).json()

        response = session.patch(baseurl + "/booking/" + str(booking_id), auth=auth, json=patch_data)

        get_af = session.get(baseurl + "/booking/" + str(booking_id)).json()

        assert get_be["firstname"] != get_af["firstname"] and get_be["lastname"] == get_af["lastname"]



# NEGATIVE TESTS

class TestBookNegative:

    def test_create_invalid_data(self, session):

        invalid_booking = {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 2345,
            "depositpaid": "False",
            "bookingdates": {
                "checkin": "2025-01-01",
                "checkout": "2026-01-01"
            },
            "additionalneeds": "dinner"
        }
        response = session.post(baseurl + "/booking", json=invalid_booking)

        assert response.status_code in (400, 500)


    def test_get_nonexistent_booking(self, session):
        response = session.get(baseurl + "/booking/999999999")

        assert response.status_code == 404


    def test_delete_without_auth(self, session, booking_id):
        response = session.delete(baseurl + "/booking/" + str(booking_id))

        assert response.status_code == 405


    def test_put_nonexistent_booking(self, session):
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
        response = session.put(baseurl + "/booking/999999999", json=updated_booking, auth=auth)

        assert response.status_code in (404, 405)


    def test_patch_empty_body(self, session, booking_id):
        response = session.patch(
            baseurl + "/booking/" + str(booking_id),
            auth=auth,
            json={}
        )

        assert response.status_code in (400, 500)