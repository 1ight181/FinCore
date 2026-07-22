FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY .env .

RUN pip install --upgrade pip \
    && pip install .

COPY . .

EXPOSE 8000

CMD ["python", "-m", "app.main"]
