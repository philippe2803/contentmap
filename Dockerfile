FROM ubuntu:22.04


RUN apt update
RUN apt install -y python3-pip libgomp1 libatlas-base-dev liblapack-dev libsqlite3-dev

WORKDIR /app

ADD poetry.lock /app/poetry.lock
ADD pyproject.toml /app/pyproject.toml

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

RUN python3 -c 'from sentence_transformers import SentenceTransformer; embedder = SentenceTransformer("all-MiniLM-L6-v2")'


ADD . /app

CMD ["pytest", "./tests"]
