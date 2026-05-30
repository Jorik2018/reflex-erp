FROM python:3.11-slim

# Instalar Node
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    unzip \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Instalar Poetry
RUN pip install poetry

WORKDIR /app

# Copiar dependencias
COPY pyproject.toml poetry.lock* /app/

# Instalar deps
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copiar código
COPY . /app

# Limpiar build previo
RUN rm -rf .web

# Compilar Reflex
RUN reflex compile

# ==============================
# 🔥 FIX OPENSHIFT PERMISSIONS
# ==============================
ENV HOME=/tmp
ENV XDG_DATA_HOME=/tmp/.local/share
ENV REFLEX_DIR=/tmp/reflex

# Crear usuario (OpenShift requirement)
RUN useradd -m appuser

USER appuser

EXPOSE 3000

CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--single-port"]