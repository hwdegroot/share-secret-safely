import json
import os
import time
from wsgi_app import app, db
from http import HTTPStatus
from unittest import TestCase
from requests.exceptions import HTTPError
from mock_alchemy.mocking import UnifiedAlchemyMagicMock


class ApiTest(TestCase):
    client = None

    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = None
        app.config["APP_SECRET_KEY"] = os.getenv("APP_SECRET_KEY")
        app.config["JSON_AS_ASCII"] = os.getenv("JSON_AS_ASCII") == "true"
        db.session = UnifiedAlchemyMagicMock()
        self.client = app.test_client()


    def tearDown(self):
        self.client = None


    def test_root_endpoint_returns_ok(self):
        response = self.client.get("/")

        self.assertEquals(HTTPStatus.OK, response.status_code)


    def test_store_empty_secret_returns_bad_request(self):
        data = { "secret": None }
        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.BAD_REQUEST, response.status_code)

        data = { "secret": "" }
        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.BAD_REQUEST, response.status_code)

        data = { "secret": "   " }
        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.BAD_REQUEST, response.status_code)


    def test_secret_stored_returns_created(self):
        data = { "secret": "secret", "expires_after_days": 1 }

        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.CREATED, response.status_code)


    def test_get_existing_secret_returns_ok(self):
        data = { "secret": "secret", "expires_after_days": 1 }

        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.CREATED, response.status_code)

        result_json = json.loads(response.data.decode())

        response = self.client.get(f"/api/v1/secret/{result_json['id']}")
        self.assertEquals(HTTPStatus.OK, response.status_code)


    def test_get_invalid_uuid_secret_returns_not_found(self):
        response = self.client.get("/api/v1/secret/00000000-0000-0000-0000-000000000000")

        self.assertEquals(HTTPStatus.NOT_FOUND, response.status_code)


    def test_get_non_existing_secret_returns_not_found(self):
        response = self.client.get("/api/v1/secret/invalid-uuid")

        self.assertEquals(HTTPStatus.NOT_FOUND, response.status_code)


    def test_get_viewed_secret_returns_forbidden(self):
        data = { "secret": "secret", "expires_after_days": 1 }

        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.CREATED, response.status_code)

        result_json = json.loads(response.data.decode())

        response = self.client.get(f"/api/v1/secret/{result_json['id']}")
        self.assertEquals(HTTPStatus.OK, response.status_code)

        response = self.client.get(f"/api/v1/secret/{result_json['id']}")
        self.assertEquals(HTTPStatus.FORBIDDEN, response.status_code)


    def test_get_expired_secret_returns_forbidden(self):
        data = { "secret": "secret", "expires_after_days": 0 }

        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.CREATED, response.status_code)
        result_json = json.loads(response.data.decode())

        time.sleep(1)

        response = self.client.get(f"/api/v1/secret/{result_json['id']}")
        self.assertEquals(HTTPStatus.FORBIDDEN, response.status_code)

    def test_get_app_version(self):
        response = self.client.get("/api/version")
        self.assertEquals(HTTPStatus.OK, response.status_code)

