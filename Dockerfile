FROM python:3.13-slim as base
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"

COPY . .
RUN chmod +x entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]