FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/ requirements/
ARG REQUIREMENTS=requirements/production.txt
RUN pip install -r $REQUIREMENTS

COPY . .

RUN find . -name "*.po" -exec sh -c 'msgfmt -o "${1%.po}.mo" "$1"' _ {} \;