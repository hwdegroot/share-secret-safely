FROM python:3.9-slim

MAINTAINER Rik de Groot <hwdegroot@gmail.com>

# Copy requirements file
COPY Pipfile /tmp/Pipfile

# Update the package lists:
RUN apt-get update

# Install wget to get the key
RUN apt-get install -y \
    build-essential \
    libpq-dev \
    python3-psycopg2 \
    postgresql-client

# Install alll known dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
RUN cd /tmp && pipenv lock -r --dev | tee /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# remove dependency file
RUN rm /tmp/Pipfile /tmp/requirements.txt

# Clean up
RUN apt-get clean autoclean
RUN apt-get autoremove --yes
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR /var/current

EXPOSE 8080
