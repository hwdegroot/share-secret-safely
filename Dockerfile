FROM python:3.9-alpine

MAINTAINER Rik de Groot <hwdegroot@gmail.com>

# Copy requirements file
COPY Pipfile /tmp/Pipfile

# Install wget to get the key
RUN apk add --update \
    g++ \
    libpq-dev \
    postgresql-dev \
    python3-dev \
    musl-dev

# Install alll known dependencies
RUN pip install --upgrade pip psycopg2-binary
RUN pip install pipenv
RUN cd /tmp && pipenv lock -r --dev | tee /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# remove dependency file
RUN rm /tmp/Pipfile /tmp/requirements.txt

# Clean up
RUN rm -f /tmp/{Pipfile,requirements.txt}

WORKDIR /var/current

EXPOSE 8080
