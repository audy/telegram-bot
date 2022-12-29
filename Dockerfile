FROM python:3.11.0

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . /app/

ENTRYPOINT ["./bot.py"]
