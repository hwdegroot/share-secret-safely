import os
from .secret import Secret
from flask_migrate import Migrate
from wsgi_app import app, db, app_dir

migrate = Migrate(app, db, directory=os.path.join(app_dir, "migrations"))

