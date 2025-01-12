FROM python:3.12.2-slim

LABEL authors="ja"

WORKDIR /FitApp

# Install necessary dependencies
RUN apt-get update && apt-get install -y curl build-essential libpq-dev && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --yes
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files and install dependencies
COPY pyproject.toml poetry.lock /FitApp/
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction

# Copy the rest of the application code
COPY . /FitApp

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]
