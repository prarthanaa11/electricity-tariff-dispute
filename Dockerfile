FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY corpus/ ./corpus/
COPY data/ ./data/
COPY evaluation/ ./evaluation/
COPY monitoring/ ./monitoring/
COPY prompts/ ./prompts/
COPY tracing/ ./tracing/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]