FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y curl build-essential unzip

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-root

COPY . .

# ❌ NO compiles aquí (esto te rompe permisos)
# RUN reflex compile


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

WORKDIR /app

COPY --from=builder /app /app

# 🔥 CLAVE OPENSHIFT FIX
ENV HOME=/tmp
ENV XDG_DATA_HOME=/tmp/.local/share
ENV REFLEX_DIR=/tmp/reflex
ENV TMPDIR=/tmp

# ❌ NO useradd (OpenShift rompe esto)
# USER appuser

EXPOSE 3000

# 🔥 IMPORTANTE: regen clean runtime
CMD ["bash", "-c", "rm -rf .web && poetry run reflex run --env prod --backend-host 0.0.0.0 --single-port"]