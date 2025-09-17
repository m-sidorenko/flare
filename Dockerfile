FROM python:3.12-slim-bookworm AS builder

# uv setup
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates libgomp1
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# copy uv file
COPY pyproject.toml /app
COPY uv.lock /app

# run uv to create a virtual environment and install dependencies
RUN uv sync --locked


FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates libgomp1
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY / /app/

ENV PATH="/app/.venv/bin:/root/.local/bin:$PATH"
ENV PYTHONPATH=/app

EXPOSE ${SERVICE_PORT:-8080}

CMD ["uv", "run", "python", "src/main.py"]