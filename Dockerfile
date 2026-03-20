FROM python:3.13-slim

RUN pip install uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src/ ./src/
RUN uv sync --frozen --no-dev

EXPOSE 8050

CMD ["/app/.venv/bin/gunicorn", "showstats.app:server", \
     "--preload", "--bind", "0.0.0.0:8050", \
     "--workers", "2", "--timeout", "120"]