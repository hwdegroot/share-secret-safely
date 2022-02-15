web: gunicorn wsgi_app:app --log-file=-
release: bash wsgi_app/migrations/migrate.sh
