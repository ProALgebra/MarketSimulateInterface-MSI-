FROM python:3.10 as bot_base
COPY bot/requirements.txt bot/requirements.txt
COPY sandbox_worker/requirements.txt sandbox_worker/requirements.txt
RUN pip install -r bot/requirements.txt
RUN pip install -r sandbox_worker/requirements.txt
COPY . .
RUN pybabel compile -d bot/locales -D mybot
CMD ["python3", "bot/bot_start.py"]
ENV PYTHONPATH "${PYTHONPATH}:/app"
