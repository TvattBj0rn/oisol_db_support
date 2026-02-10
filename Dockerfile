# Stage 1
FROM python:3.14.0-slim as builder
LABEL authors="Vask"
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . /app
RUN uv sync

# Stage 2
FROM python:3.14.0-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY . .
ENTRYPOINT ["uv", "run", "main.py"]
CMD ["test"]
