#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler

from neighborhoods import NEIGHBORHOODS

import random
import requests
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

updater = Updater(
    token="636614158:AAEDn80O9QQyOq5PW1a8lk1Yb2SUhBlny2I", use_context=True
)


def cat(update, context):
    """ a random cat photo """
    resp = requests.get("https://api.thecatapi.com/v1/images/search?size=full")
    cat_url = resp.json()[0]["url"]
    context.bot.send_message(chat_id=update.message.chat_id, text=cat_url)


def hood(update, context):
    """ a random neighborhood in SF """
    neighborhood = random.choice(NEIGHBORHOODS)
    context.bot.send_message(chat_id=update.message.chat_id, text=neighborhood)


def joke(update, context):
    """ tell a joke """
    resp = requests.get(
        "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
    )
    joke = resp.json()["joke"]
    context.bot.send_message(chat_id=update.message.chat_id, text=joke)


def weather(update, context):
    resp = requests.get(
        "https://api.darksky.net/forecast/d3e344b04f2da052a8b96431bf58131d/37.8267,-122.4233"
    )

    weather_data = resp.json()

    weather_summary = f"""
Currently: {weather_data['minutely']['summary']}
(Wind={weather_data['currently']['windSpeed']}-mph; Temp={weather_data['currently']['temperature']}-F Humidity={100*weather_data['currently']['humidity']}%)
Today: {weather_data['hourly']['summary']}
Forecast: {weather_data['daily']['summary']}
"""

    context.bot.send_message(chat_id=update.message.chat_id, text=weather_summary)


commands = {"cat": cat, "hood": hood, "joke": joke, "weather": weather}

for command_name, command_function in commands.items():
    updater.dispatcher.add_handler(CommandHandler(command_name, command_function))

print("listening")
updater.start_polling()
