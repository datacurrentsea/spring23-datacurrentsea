# Dockerfile
# Build venv
#FROM python:3.10-buster as venv
FROM python:3.10-slim as venv

RUN apt-get update \
    && apt-get install -y \
        curl \
        build-essential \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.3.1
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH /root/.local/bin:$PATH

# Install Dependencies
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && poetry install

# Build runtime image
FROM python:3.10-slim-buster as prod
COPY --from=venv /app/venv/ /app/venv/
ENV PATH /app/venv/bin:$PATH

WORKDIR /app
COPY . ./

HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"

CMD ["uvicorn","src.main:app","--host","0.0.0.0","--port","8000"]