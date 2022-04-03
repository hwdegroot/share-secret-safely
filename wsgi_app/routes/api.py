from flask import (
    jsonify,
    redirect,
    request,
    url_for,
)
import os
from wsgi_app import app
from .utils import (
    create_secret_link,
    store_secret,
    obtain_secret
)
from wsgi_app.exceptions import (
    InvalidSecretIdentifierException,
    SecretNotFoundException,
    SecretAlreadyViewedException,
    SecretExpiredException
)

API_PREFIX = "/api/v1"

DAY_IN_SECONDS = 3600 * 24


@app.route("/api/v1/secret/store", methods=["POST"])
def api_store():
    """
    Check if the secret is more than just a space
    """
    data = request.get_json(force=True)
    secret = data.get("secret", "")
    expires_after = data.get("expires_after_days", None)
    ttl = DAY_IN_SECONDS * expires_after if isinstance(expires_after, int) else None

    if secret.isspace():
        return jsonify({
            "error": "Please provide a secret",
        }), 400

    secret_id = store_secret(secret, ttl=ttl)
    api_link = create_secret_link(secret_id, prefix=API_PREFIX)
    link = create_secret_link(secret_id)
    return jsonify({
        "api_link": api_link,
        "link": link,
        "expires_after_days": expires_after
    }), 201


@app.route("/api/v1/secret/<uuid:secret_id>", methods=["GET"])
def api_get_secret(secret_id):
    try:
        secret = obtain_secret(secret_id)
    except InvalidSecretIdentifierException:
        return jsonify({
            "error": f"Id {secret_id} is not a valid guid",
        }), 404
    except SecretNotFoundException:
        return jsonify({
            "error": f"Secret {secret_id} does not exist",
        }), 404
    except SecretAlreadyViewedException:
        return jsonify({
            "error": f"Secret {secret_id} has already been viewed",
        }), 403

    except SecretExpiredException:
        return jsonify({
            "error": f"Secret {secret_id} viewing has expired",
        }), 403

    return jsonify({
        "secret": secret
    }), 200
