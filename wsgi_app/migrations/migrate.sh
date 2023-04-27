#!/usr/bin/env bash

echo "===== Initalize the database ====="
flask db stamp head
if ! [[ -d wsgi_app/migrations ]]; then
    flask db init
else
    echo "DB already initialized. Skipping"
fi

echo "===== Run the migrations ====="
flask db migrate

echo "===== Upgrade the database ====="
flask db upgrade
