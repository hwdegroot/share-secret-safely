#!/usr/bin/env bash

echo "===== Initalize the database ====="
flask db init

echo "===== Run the migrations ====="
flask db migrate

echo "===== Upgrade the database ====="
flask db upgrade
