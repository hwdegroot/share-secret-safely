#!/bin/bash

npm install
npm run build

if [[ " $* " =~ " --serve " ]]; then
    node_modules/.bin/nodemon \
        --watch src \
        --watch wsgi_app/templates \
        --exec 'npm run build'
fi

