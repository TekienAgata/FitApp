FROM python:3.12.2-slim

LABEL authors="ja"

WORKDIR /FitApp

# Install necessary dependencies
RUN apt-get update && apt-get install -y curl build-essential libpq-dev && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --yes
ENV PATH="/root/.local/bin:$PATH"

# Copy only dependency files first
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction

# We don't need to copy the application code here anymore since we'll use volumes
# The code will be mounted at runtime

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0", "--debug"]