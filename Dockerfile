FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y curl build-essential unzip

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-root

COPY . .


# ======================
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    ca-certificates \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip install poetry \
 && pip install reflex

# 🔥 CLAVE REAL: todo en /tmp
WORKDIR /tmp/app

COPY --from=builder /app /tmp/app

ENV HOME=/tmp
ENV TMPDIR=/tmp
ENV XDG_DATA_HOME=/tmp/.local/share
ENV REFLEX_DIR=/tmp/reflex
ENV REFLUX_DIR=/tmp/reflex
ENV PYTHONUSERBASE=/tmp/python

EXPOSE 3000

CMD ["bash", "-c", "cd /tmp/app && export HOME=/tmp && export TMPDIR=/tmp && poetry run reflex run --env prod --backend-host 0.0.0.0 --single-port --loglevel debug"]