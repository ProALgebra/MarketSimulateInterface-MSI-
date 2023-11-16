FROM python:3.11-slim-buster as bot_base
COPY bot_app/requirements.txt /app/bot_app/requirements.txt
COPY shared/requirements.txt /app/shared/requirements.txt
RUN pip install -r /app/bot_app/requirements.txt

FROM bot_base

COPY ../bot /app/bot_app
COPY ../shared /app/shared
WORKDIR /app/bot_app
RUN pybabel compile -d /app/bot_app/locales -D messages
ENV PYTHONPATH "${PYTHONPATH}:/app"
