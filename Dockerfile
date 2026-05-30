FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl build-essential unzip \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app

# =========================
# FIX OPENSHIFT PERMISSIONS
# =========================
ENV HOME=/tmp
ENV XDG_DATA_HOME=/tmp/.local/share
ENV REFLEX_DIR=/tmp/reflex

RUN useradd -m appuser
USER appuser

# 🔥 IMPORTANT: compile AFTER user switch
RUN rm -rf .web && reflex compile

EXPOSE 3000

CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--single-port"]