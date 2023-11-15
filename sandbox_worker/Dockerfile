FROM python:3.11
WORKDIR /app


COPY . .



RUN pip install -r /app/sandbox_worker/requirements.txt


CMD ["dramatiq", "sandbox_worker.worker"]