#!/bin/bash

npm install
npx tailwindcss -i wsgi_app/static/src/main.tailwind -o wsgi_app/static/css/main.css

if [[ " $* " =~ " --serve " ]]; then
    node_modules/.bin/nodemon \
        --watch wsgi_app/static/src \
        --watch wsgi_app/templates \
        --exec 'npx tailwindcss -i wsgi_app/static/src/main.tailwind -o wsgi_app/static/css/main.css'
fi

