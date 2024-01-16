FROM python:3.12

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]
