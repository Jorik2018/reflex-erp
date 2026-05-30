FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y curl build-essential unzip

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-root

COPY . .

RUN reflex compile


# ======================
FROM python:3.11-slim

RUN pip install poetry

WORKDIR /app

COPY --from=builder /app /app

ENV HOME=/tmp
ENV XDG_DATA_HOME=/tmp/.local/share
ENV REFLEX_DIR=/tmp/reflex

RUN useradd -m appuser
USER appuser

EXPOSE 3000

CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--single-port"]