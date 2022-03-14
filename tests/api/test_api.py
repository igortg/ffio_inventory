from flask.testing import FlaskClient


def test_is_alive(api: FlaskClient) -> None:
    r = api.get("is_alive")
    assert r.status_code == 200
