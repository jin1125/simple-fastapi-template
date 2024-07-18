FROM python:3.12

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

ENTRYPOINT ["fastapi", "dev", "api/main.py", "--host", "0.0.0.0"]
