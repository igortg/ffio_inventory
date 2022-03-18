import os
from pathlib import Path

from flask import Flask
from flask.testing import FlaskClient

from ffio_inventory.core import UPLOAD_FOLDER


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


def test_csv_upload(flask_app: Flask, api: FlaskClient, datadir: Path) -> None:
    csv_file_path = datadir / "sample.csv"
    with csv_file_path.open("rb") as csv_file:
        r = api.post(
            "/product/upload-csv",
            data={'file': (csv_file, csv_file_path.name)},
            content_type='multipart/form-data',
        )
        assert r.status_code == 201
        assert r.json == "11 products added"

    assert os.listdir(UPLOAD_FOLDER) == ['sample.csv']
