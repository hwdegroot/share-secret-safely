import os
from wsgi_app.factory import Factory
from cryptography.fernet import Fernet


# require environment variables
envvar_required = [
    "APP_SECRET_KEY",
    "ENCRYPTION_SALT",
]

for envvar in envvar_required:
    if envvar not in os.environ:
        raise ValueError(f"Environment variable {envvar} is required. Make sure it is set")

app_dir = os.path.dirname(__file__)
app_factory = Factory(
    template_folder=os.path.join(app_dir, "templates"),
    static_folder=os.path.join(app_dir, "static")
)
app = app_factory.create_app()
app.secret_key = os.getenv("APP_SECRET_KEY")

db = app_factory.get_db(app)

logger = app_factory.get_logger()

# Cipher to hash and unhash secrets
# https://cryptography.io/en/latest/
ENCRYPTION_SALT = os.getenv('ENCRYPTION_SALT').encode("utf-8")
cipher = Fernet(ENCRYPTION_SALT)

# Load our routes here
import wsgi_app.routes

if __name__ == "__main__":
    app.run()
