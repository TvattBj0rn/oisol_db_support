FROM python:3.14.0-alpine
LABEL authors="Vask"
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . /app
RUN uv sync
ENTRYPOINT ["uv", "run", "main.py"]
CMD ["test"]