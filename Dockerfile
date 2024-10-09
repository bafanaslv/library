FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root
COPY . .
