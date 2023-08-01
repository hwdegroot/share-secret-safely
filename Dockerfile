FROM python:3.11.4-alpine

MAINTAINER Rik de Groot <hwdegroot@gmail.com>

# Copy requirements file
COPY Pipfile /tmp/Pipfile
COPY Pipfile.lock /tmp/Pipfile.lock

RUN apk add --update --no-cache --virtual .build-deps curl jq
RUN apk add bash git

# Find the latest release of delta, for fancy diffing
RUN curl -sSL -H"Accept: application/vnd.github.v3+json" "https://api.github.com/repos/dandavison/delta/releases?per_page=1" | \
        jq -r '.[].assets | .[].browser_download_url' | \
        grep 'delta-[0-9.]*-x86_64-unknown-linux-gnu.tar.gz' > /tmp/git-delta
RUN cat /tmp/git-delta | xargs -i curl -sSL {} -o /tmp/delta.tar.gz
RUN tar -C /tmp --strip-components 1 -xzvf /tmp/delta.tar.gz
RUN mv -v /tmp/delta /usr/local/bin


# Install wget to get the key
RUN apk add --update \
    g++ \
    libffi-dev \
    libpq-dev \
    postgresql-dev \
    python3-dev \
    musl-dev

# Install alll known dependencies
RUN pip install --upgrade pip psycopg2-binary
RUN pip install pipenv
RUN cd /tmp && pipenv requirements --dev | tee /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# remove dependency file
RUN apk del .build-deps
RUN rm -rf /tmp/Pipfile /tmp/Pipfile.lock /tmp/requirements.txt
RUN git config --global --add safe.directory /var/current

WORKDIR /var/current

EXPOSE 8080
