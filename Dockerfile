FROM python:3.12-slim AS builder

ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential && \
    git clone --depth 1 https://github.com/Pedrofran682/FindMyBus.git . && \
    curl -sSL https://install.python-poetry.org | python3 - --version 2.2.1 && \
    poetry install --no-root --only main


FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src"

WORKDIR /app

COPY --from=builder /app /app

RUN useradd -m appuser
USER appuser

CMD ["python", "--version"]