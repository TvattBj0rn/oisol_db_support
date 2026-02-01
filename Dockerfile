FROM python:3.14
LABEL authors="Vask"
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . /app
RUN uv sync
ENTRYPOINT ["python", "main.py"]
CMD ["test"]