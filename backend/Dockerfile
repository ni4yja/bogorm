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

RUN SECRET_KEY=build-only \
    DATABASE_URL=postgis://x:x@localhost/x \
    DJANGO_SETTINGS_MODULE=config.settings.local \
    python manage.py compilemessages