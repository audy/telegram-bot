FROM python:3.8

ADD requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
ADD * /app/

ENTRYPOINT ["./bot.py"]
