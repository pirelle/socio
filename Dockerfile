FROM python:3.11.6-bookworm

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.3.1

RUN apt update && apt -y install gcc

WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt

# Creating folders, and files for a project:
COPY src /code/src
COPY alembic /code/alembic
COPY Makefile /code
COPY alembic.ini /code

#RUN chmod +x /code/src/entrypoint.sh
#CMD ["entrypoint.sh"]
