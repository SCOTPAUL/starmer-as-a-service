# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction

COPY keiths /app/keiths
COPY starmer_as_a_service /app/starmer_as_a_service

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "main:app", "--chdir", "starmer_as_a_service/"]
