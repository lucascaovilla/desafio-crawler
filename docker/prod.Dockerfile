FROM python:alpine3.22

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && pip install poetry
RUN poetry install --no-dev

ENTRYPOINT ["python", "main.py"]
