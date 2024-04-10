FROM python:3.9-slim

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install poetry

ENV VIRTUAL_ENV "/opt/venv"

ENV PATH "$VIRTUAL_ENV/bin:$PATH"

COPY app/poetry.lock app/pyproject.toml /app/

RUN python -m venv $VIRTUAL_ENV \
  && poetry install --with=dev

COPY docker/entrypoint.sh /entrypoint/entrypoint.sh

COPY app /app

ENTRYPOINT ["/entrypoint/entrypoint.sh"]
