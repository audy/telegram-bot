FROM python:3.7

ADD requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
ADD * /app/

ENTRYPOINT ["./bot.py"]
