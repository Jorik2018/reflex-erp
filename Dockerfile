FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y \
    curl build-essential unzip \
 && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

COPY . .

# (opcional pero recomendado)
RUN reflex compile || true


# ======================
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl unzip ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN pip install poetry reflex

WORKDIR /app

COPY --from=builder /app /app

# 🔥 OpenShift-safe writable dirs
ENV HOME=/tmp
ENV TMPDIR=/tmp
ENV XDG_DATA_HOME=/tmp/.local/share
ENV REFLEX_DIR=/tmp/reflex

# 🔥 CLAVE: evita conflictos de .web en root del repo
ENV REFLEX_WORKDIR=/tmp/app
RUN mkdir -p /tmp/app

WORKDIR /app

EXPOSE 3000

CMD ["bash", "-c", "\
export HOME=/tmp && \
export TMPDIR=/tmp && \
export REFLEX_DIR=/tmp/reflex && \
cd /app && \
reflex run --env prod --backend-host 0.0.0.0 --single-port --loglevel debug \
"]