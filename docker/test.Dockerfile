FROM python:3.13-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install poetry
RUN poetry install --with dev

ENTRYPOINT ["poetry", "run"]
