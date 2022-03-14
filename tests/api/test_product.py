from flask.testing import FlaskClient


def test_crud(api: FlaskClient) -> None:
    r = api.post("/product", json={"name": "Boots", "sku": "03291"})
    assert r.status_code == 201
    assert r.json["name"] == "Boots"
    assert r.json["sku"] == "03291"
    assert r.json["_id"] is not None

    r = api.get("/product")
    assert r.status_code == 200
    data_list = r.json
    assert data_list[0]["name"] == "Boots"
    assert data_list[0]["sku"] == "03291"
    assert data_list[0]["_id"] is not None
