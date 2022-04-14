#!/usr/bin/env bash

# initialize migrations
echo "========= Init the database ============="
if ! [[ -d wsgi_app/migrations ]]; then
    flask db init
fi
# run migrations
echo "========= Run all migrations ============"
flask db migrate
# upgrade db
echo "========= Upgrade DB ===================="
flask db upgrade

# and finally run the app
echo "========= Run the app ==================="

if [[ "FLASK_ENV" = "production" ]] || [[ "ENVIRONMENT" = "production" ]]; then
    ./gunicorn.sh --bind=0.0.0.0:8080
else
    flask run
fi
