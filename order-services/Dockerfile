FROM python:3.12
LABEL maintainer="Abdullah-Asif"

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    protobuf-compiler \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*


RUN pip install poetry

COPY . /code/

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-root 

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


