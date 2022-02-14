# Secret sharing

Share secrets safely

## Getting started

Run locally

    make run

## Update database

run

    flask db revision -m "<revision name>" --autogenerate

## Migrate

run

    flask db upgrade

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
