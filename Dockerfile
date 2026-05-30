FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl unzip ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry reflex

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# OpenShift-safe env
ENV HOME=/tmp \
    TMPDIR=/tmp \
    XDG_DATA_HOME=/tmp/.local/share \
    REFLEX_DIR=/tmp/reflex

EXPOSE 3000

CMD ["bash", "-c", "\
cd /tmp && \
cp -r /app/. . && \
rm -rf .web && \
reflex run --env prod --backend-host 0.0.0.0 --single-port --loglevel debug \
"]