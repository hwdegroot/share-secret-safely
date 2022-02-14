from flask import (
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.exceptions import Forbidden, NotFound
import os
from wsgi_app import app
from uuid import UUID
from .utils import (
    create_secret_link,
    store_secret,
    obtain_secret
)
from wsgi_app.exceptions import (
    InvalidSecretIdentifierException,
    SecretNotFoundException,
    SecretAlreadyViewedException
)


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/secret/<uuid:secret_id>")
def secret(secret_id):
    try:
        secret = obtain_secret(secret_id)
    except InvalidSecretIdentifierException:
        abort(404, f"Id {secret_id} is not a valid guid")
    except SecretNotFoundException:
        abort(404, f"Secret {secret_id} does not exist")
    except SecretAlreadyViewedException:
        abort(403, f"Secret{secret_id} has already been viewed")

    return render_template("show_secret.html", secret=secret)


@app.route("/store", methods=["POST"])
def save_secret():
    """
    Store secret in the database
    """
    if request.form.get("secret", "").isspace():
        flash("Please provide a secret")
        return redirect(url_for("index"), 400)

    secret_id = store_secret(request.form.get("secret", ""))

    # return hash
    return redirect(url_for("stored_secret", id=secret_id))


@app.route("/store", methods=["GET"])
def stored_secret():
    # Check if the id argument is in the wuer
    if not request.args.get("id"):
        abort(404)

    secret_id = request.args.get("id")

    # Try parsing the id to a UUID
    try:
        UUID(secret_id)
    except ValueError:
        abort(404)

    link = create_secret_link(secret_id)
    # return hash
    return render_template(
        "stored_secret.html",
        link=link
    )


@app.errorhandler(NotFound)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(Forbidden)
def forbidden(e):
    return render_template('403.html'), 404
