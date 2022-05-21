import os
import sys
import time
import unittest
from uuid import uuid4
from wsgi_app import cipher, db
from wsgi_app.models import Secret
from wsgi_app.routes.utils import (
    create_secret_link,
    store_secret,
    obtain_secret,
    is_valid_guid
)
from wsgi_app.exceptions import (
    InvalidSecretIdentifierException,
    SecretNotFoundException,
    SecretAlreadyViewedException,
    SecretExpiredException
)
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from cryptography.fernet import Fernet


class PasswordEncodingTest(unittest.TestCase):

    def setUp(self):
        db.session = UnifiedAlchemyMagicMock()
        os.environ["ENCRYPTION_SALT"] = Fernet.generate_key().decode()


    def test_environment_variables_are_set(self):
        envvar_required = [
            "APP_SECRET_KEY",
            "ENCRYPTION_SALT",
        ]

        for envvar in envvar_required:
            self.assertIn(envvar, os.environ, f"environment {envvar} not set")


    def test_encrypting_secret_should_return_secret_id(self):
        secret_id = store_secret("secret")
        self.assertTrue(is_valid_guid(secret_id))


    def test_decrypting_hashed_secret_should_return_secret(self):
        SECRET = "secret_3 30"
        token = cipher.encrypt(bytes(SECRET, "utf-8"))
        # Create a secret object from the string
        secret = Secret(bytes.decode(token))
        # actually store the secret
        db.session.add(secret)
        secret_value = obtain_secret(secret.id)

        self.assertEqual(SECRET, secret_value)


    def test_retrieving_secret_wipes_value_in_db(self):
        SECRET = "secret_3 30"
        token = cipher.encrypt(bytes(SECRET, "utf-8"))
        # Create a secret object from the string
        secret = Secret(bytes.decode(token))
        # actually store the secret
        db.session.add(secret)
        secret_value = obtain_secret(secret.id)

        self.assertEqual(SECRET, secret_value)
        wipedSecret = db.session.query(Secret).filter(Secret.id == str(secret.id)).first()
        self.assertIsNone(wipedSecret.encoded_secret)


    def test_decrypting_hashed_secret_ttl_expired_should_throw_SecretExpiredException(self):
        secret_id = store_secret("secret", ttl=0)
        time.sleep(1)

        self.assertRaises(SecretExpiredException, obtain_secret, secret_id)


    def test_decrypting_hashed_secret_second_time_should_throw_SecretAlreadyViewedException(self):
        secret_id = store_secret("secret")
        obtain_secret(secret_id)

        self.assertRaises(SecretAlreadyViewedException, obtain_secret, secret_id)

    def test_decrypting_not_existing_secret_should_throw_SecretNotFoundEception(self):
        self.assertRaises(SecretNotFoundException, obtain_secret, str(uuid4()))


    def test_decrypting_invalid_secret_guid_should_throw_InvalidSecretIdentifierException(self):
        self.assertRaises(InvalidSecretIdentifierException, obtain_secret, "abcdfg")
