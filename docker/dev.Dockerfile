FROM python:alpine3.22

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && pip install poetry
RUN poetry install --with dev

ENTRYPOINT ["poetry", "run", "python", "main.py"]
