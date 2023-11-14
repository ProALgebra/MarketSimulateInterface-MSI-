FROM python:3.11-slim-buster as alembic_base
COPY alembic/requirements.txt /app/alembic/requirements.txt
COPY shared/requirements.txt /app/shared/requirements.txt
RUN pip install -r /app/alembic/requirements.txt

FROM alembic_base
COPY ../shared /app/shared
COPY ../alembic /app/alembic
COPY ../alembic.ini /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app
