FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install -y libgdal-dev

RUN pip install GDAL==3.6.0

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip3 install poetry

RUN poetry install --no-dev

COPY _scripts/init.sh ./
