# Secret sharing

Need a safe way to share secrets with people. With this tool you can lock a secret safely encrypted, available to
view only once.

Also supports an api to lock and share secrets.

Build with [Python-Flask](https://flask.palletsprojects.com/en/2.0.x/) and [tailwindcss](https://tailwindcss.com/)

Share secrets safely.

## Getting started

Run locally

    make run

When running in production, make sure to use a different `ENCRYPTION_SALT`. You can generate one, using
`Fernet.generate_key()`.

More info in the [cryptography docs](https://pypi.org/project/cryptography/)

### Linting the code

When the app is running locally, run

    make autoformat

## Update database

run

    flask db revision -m "<revision name>" --autogenerate

## Migrate

Locally the migrations will run when running the app.
To run migrations manually, run

    wsgi_app/migrations/migrate.sh

## Creating the database

```python
with app.app_context():
    db.create_all()
```

## Api

Store a new secret by posting it to the api

    curl -XPOST -H"Content-Type: application/json" -d '{"secret": "secret"}' localhost:8080/api/v1/secret/store

This will return two links

```json
{
    "link": "/secret/<hash>",
    "api_link": "/api/v1/secret/<hash>"
}
```

You can obtain the secret (once) by opening the url in the browser, or getting it from the api

    curl -XGET  localhost:8080/api/v1/secret/<hash>

The api call will return a json with your secret

```json
{
    "secret": "Your secret"
}
```

## Test

Run the unittest like so

    python wsgi_app/run_test.py

## Heroku local

    pipenv install
    pipenv shell
    heroku local web --env=.env.local
