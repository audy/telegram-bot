FROM python:3.9.0

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH=/root/.poetry/bin:$PATH

WORKDIR /app

ADD pyproject.toml .

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction

ADD . /app/

ENTRYPOINT ["./bot.py"]
