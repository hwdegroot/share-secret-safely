from flask import (
    abort,
    request,
    url_for,
)
import os
import re
from cryptography.fernet import InvalidToken
from wsgi_app import cipher, db, app
from wsgi_app.models import Secret
from wsgi_app.exceptions import (
    InvalidSecretIdentifierException,
    SecretNotFoundException,
    SecretAlreadyViewedException,
    SecretExpiredException
)


def create_secret_link(secret_id, **kwargs):
    """
    Create secret link for api and non api usage
    """
    prefix = kwargs["prefix"] if "prefix" in kwargs and kwargs["prefix"] else ""
    return "{}{}{}".format(
        request.host_url.rstrip("/"),
        prefix,
        url_for("secret", secret_id=secret_id)
    )


def store_secret(secret_value, ttl=None):
    """
    Dump secret in the database
    """
    # if empty return back
    token = cipher.encrypt(bytes(secret_value, "utf-8"))

    # Create a secret object from the string
    secret = Secret(token, ttl=ttl)
    # actually store the secret
    db.session.add(secret)
    db.session.commit()

    return str(secret.id)


def obtain_secret(secret_id, verify=False):
    """
    Fetch the secret from the database
    """
    if not is_valid_guid(str(secret_id)):
        raise InvalidSecretIdentifierException(f"{secret_id} is not a valid guid")

    secret = db.session.query(Secret).filter(Secret.id == str(secret_id)).first()
    # Secret not available
    if secret is None:
        raise SecretNotFoundException("Secret does not exist")

    # 403 when already viewed
    if secret.encoded_secret is None:
        raise SecretAlreadyViewedException(403)

    try:
        secret_value = cipher.decrypt(secret.encoded_secret, ttl=secret.ttl)
    except InvalidToken:
        if not verify:
            secret.encoded_secret = None
            db.session.add(secret)
            db.session.commit()
        raise SecretExpiredException(403)

    # set the value to None so we know it has been viewed
    if not verify:
        secret.encoded_secret = None
        db.session.add(secret)
        db.session.commit()

        return secret_value.decode()

    return None


def is_valid_guid(value):
    """
    Check that string is a valid guid
    """
    # Regex to check valid
    # GUID (Globally Unique Identifier)
    regex = r"^[{]?[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}[}]?$"

    # Compile the ReGex
    compiled_regex = re.compile(regex)

    # If the string is empty
    # return false
    if str is None:
        return False

    # Return if the string
    # matched the ReGex
    return compiled_regex.search(value) is not None
