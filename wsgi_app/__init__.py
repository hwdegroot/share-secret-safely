import os
from wsgi_app.factory import Factory
from cryptography.fernet import Fernet
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.httpx import HttpxIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration


# Setup the Flask-JWT-Extended extension

# require environment variables
envvar_required = [
    "APP_SECRET_KEY",
    "ENCRYPTION_SALT",
    "JWT_SECRET_KEY",
]
# Require a bunch of app
for envvar in envvar_required:
    if envvar not in os.environ:
        raise ValueError(f"Environment variable {envvar} is required. Make sure it is set")

# Setup application
app_dir = os.path.dirname(__file__)
app_factory = Factory(
    template_folder=os.path.join(app_dir, "templates"),
    static_folder=os.path.join(app_dir, "static")
)
# Under water this calls Flask(__name__)
app = app_factory.create_app()
# Setup the session secret key
app.secret_key = os.getenv("APP_SECRET_KEY")
# Initialize the database
# WIll call db.init_app(app)
db = app_factory.get_db(app)
# Initialize logger alias.
# Calls app.getLogger()
logger = app_factory.get_logger()

# Cipher to hash and unhash secrets
# https://cryptography.io/en/latest/
ENCRYPTION_SALT = os.getenv('ENCRYPTION_SALT').encode("utf-8")
cipher = Fernet(ENCRYPTION_SALT)

if os.getenv("SENTRY_DSN", "").strip() != "":
    sample_rate = parse_float(os.getenv("SENTRY_SAMPLE_RATE"), default=0.5)
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[
            FlaskIntegration(),
            HttpxIntegration(),
            SqlalchemyIntegration(),
        ],
        environment=os.getenv("SENTRY_ENVIRONMENT", "production"),
        max_breadcrumbs=50,
        debug=os.getenv("SENTRY_ENVIRONMENT") != "production",
        release=os.getenv("APP_VERSION", "dev"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=sample_rate
    )

# Load our routes here
import wsgi_app.routes

if __name__ == "__main__":
    app.run()
