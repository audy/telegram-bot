FROM python:3.7

WORKDIR /app
ADD * /app/

RUN pip install -r requirements.txt

ENTRYPOINT ["./bot.py"]
