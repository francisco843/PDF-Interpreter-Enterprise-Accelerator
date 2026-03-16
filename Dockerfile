FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md PROJECT_REQUIREMENTS.md ./
COPY src ./src
COPY configs ./configs
COPY data/external ./data/external

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

CMD ["pdf-interpreter", "train", "--config", "configs/base.yaml"]
