FROM python:3.10 as bot_base
COPY . .
RUN pip install -r bot/requirements.txt
RUN pip install -r sandbox_worker/requirements.txt
RUN pybabel compile -d bot/locales -D mybot
CMD ["python3", "bot/bot_start.py"]
ENV PYTHONPATH "${PYTHONPATH}:/app"
