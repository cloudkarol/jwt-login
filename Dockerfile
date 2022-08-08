FROM python:3.8-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 

# System deps:
RUN pip install "poetry"

# Copy only requirements to cache them in docker layer
WORKDIR /src
COPY poetry.lock pyproject.toml /src/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /src
ENTRYPOINT ./entrypoint.sh