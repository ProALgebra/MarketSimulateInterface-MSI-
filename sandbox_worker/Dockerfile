FROM python:3.12
WORKDIR /app


COPY . .



RUN pip install -r /app/sandbox_worker/requirements.txt


CMD ["dramatiq", "sandbox_worker.worker.run_sandbox"]