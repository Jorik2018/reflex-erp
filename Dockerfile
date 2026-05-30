FROM python:3.11-slim

# Instalar Node
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Instalar Poetry
RUN pip install poetry

WORKDIR /app

# Copiar dependencias
COPY pyproject.toml poetry.lock* /app/

# Instalar deps
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copiar código
COPY . /app

# Limpiar build previo
RUN rm -rf .web

# Compilar Reflex
RUN reflex compile

# Crear usuario (OpenShift requirement)
RUN useradd -m appuser
USER appuser

EXPOSE 3000

# Ejecutar app
CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--frontend-host", "0.0.0.0"]