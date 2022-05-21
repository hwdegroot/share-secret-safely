import json
import os
from unittest.mock import patch
import time
from wsgi_app import app, db
from http import HTTPStatus
from unittest import TestCase
from requests.exceptions import HTTPError
from flask_jwt_extended import create_access_token
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

class UiTest(TestCase):
    client = None

    def setUp(self):
        app.config["APP_SECRET_KEY"] = os.getenv("APP_SECRET_KEY")
        app.config["JSON_AS_ASCII"] = os.getenv("JSON_AS_ASCII") == "true"
        self.client = app.test_client()
        db.session = UnifiedAlchemyMagicMock()


    def test_secret_endpoint_returns_ok(self):
        data = { "secret": "secret", "expires_after_days": 1 }

        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.CREATED, response.status_code)
        result_json = json.loads(response.data.decode())

        response = self.client.get("/store", query_string={"id": result_json["id"]})
        self.assertEquals(HTTPStatus.OK, response.status_code)


    def test_secret_endpoint_no_id_returns_not_found(self):
        data = { "secret": "secret", "expires_after_days": 1 }

        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.CREATED, response.status_code)
        result_json = json.loads(response.data.decode())

        response = self.client.get("/store")
        self.assertEquals(HTTPStatus.NOT_FOUND, response.status_code)


    def test_secret_endpoint_invalid_id_returns_not_found(self):
        data = { "secret": "secret", "expires_after_days": 1 }

        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.CREATED, response.status_code)
        result_json = json.loads(response.data.decode())

        response = self.client.get("/store", query_string={"id": "invalid"})
        self.assertEquals(HTTPStatus.NOT_FOUND, response.status_code)


    def test_store_empty_secret_returns_bad_request(self):
        data = { "secret": None }
        response = self.client.post("/store", data=data, follow_redirects=True)
        self.assertEquals(HTTPStatus.BAD_REQUEST, response.status_code)

        data = { "secret": "" }
        response = self.client.post("/store", data=data, follow_redirects=True)
        self.assertEquals(HTTPStatus.BAD_REQUEST, response.status_code)

        data = { "secret": "   " }
        response = self.client.post("/store", data=data, follow_redirects=True)
        self.assertEquals(HTTPStatus.BAD_REQUEST, response.status_code)


    def test_secret_stored_returns_created(self):
        data = { "secret": "secret", "expires_after_days": 1 }

        response = self.client.post("/store", data=data, follow_redirects=True)
        self.assertEquals(HTTPStatus.OK, response.status_code)
        self.assertEquals(response.request.path, "/store")


    def test_get_existing_secret_async_returns_ok(self):
        data = { "secret": "secret", "expires_after_days": 0 }

        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.CREATED, response.status_code)

        result_json = json.loads(response.data.decode())

        with app.app_context():
            access_token = create_access_token(identity=result_json["id"])
            response = self.client.get(f"/api/secret/{result_json['id']}")
            self.assertEquals(HTTPStatus.UNAUTHORIZED, response.status_code)

            response = self.client.get(f"/api/secret/{result_json['id']}?access_token={access_token}")
            self.assertEquals(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_get_existing_secret_returns_ok(self):
        data = { "secret": "secret", "expires_after_days": 1 }

        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.CREATED, response.status_code)

        result_json = json.loads(response.data.decode())

        response = self.client.get(f"/secret/{result_json['id']}")
        self.assertEquals(HTTPStatus.OK, response.status_code)

    def test_get_invalid_uuid_secret_returns_not_found(self):
        response = self.client.get("/secret/00000000-0000-0000-0000-000000000000")

        self.assertEquals(HTTPStatus.NOT_FOUND, response.status_code)

    def test_get_non_existing_secret_returns_not_found(self):
        response = self.client.get("/secret/invalid-uuid")

        self.assertEquals(HTTPStatus.NOT_FOUND, response.status_code)

    def test_get_viewed_secret_returns_forbidden(self):
        data = { "secret": "secret", "expires_after_days": 1 }

        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.CREATED, response.status_code)

        result_json = json.loads(response.data.decode())

        with app.app_context():
            access_token = create_access_token(identity=result_json["id"])
            headers = { "Authorization": f"Bearer {access_token}" }
            response = self.client.get(f"/api/secret/{result_json['id']}", headers=headers)
            self.assertEquals(HTTPStatus.OK, response.status_code)

            response = self.client.get(f"/secret/{result_json['id']}")
            self.assertEquals(HTTPStatus.FORBIDDEN, response.status_code)


    def test_get_expired_secret_returns_forbidden(self):
        data = { "secret": "secret", "expires_after_days": 0 }

        response = self.client.post("/api/v1/secret/store", json=data)
        self.assertEquals(HTTPStatus.CREATED, response.status_code)
        result_json = json.loads(response.data.decode())

        time.sleep(1)

        response = self.client.get(f"/secret/{result_json['id']}")
        self.assertEquals(HTTPStatus.FORBIDDEN, response.status_code)
