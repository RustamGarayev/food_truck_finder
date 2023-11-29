FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip3 install poetry

RUN poetry install --no-dev

COPY scripts/init.sh ./
