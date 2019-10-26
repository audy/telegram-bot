#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler

from neighborhoods import NEIGHBORHOODS

import random
import requests
import logging
from yelpapi import YelpAPI

YELP_API_KEY = "q1CJG9aPlwTzWx_l-O6eEJ_YE9Dnz4Ej1Y8iN3BT5xxsa_qetRrxqhNQxDLVjcE_R6V-oSWFRoRk_C-u8HZxxmq1ZeXISygpgo2I-e675dn-cymOrRmjforBp5KzXXYx"
yelp = YelpAPI(YELP_API_KEY)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

updater = Updater(
    token="636614158:AAEDn80O9QQyOq5PW1a8lk1Yb2SUhBlny2I", use_context=True
)


def start(update, context):
    """ default /start reply """
    text = """ try /cat /hood /joke /weather """
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


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

    context.bot.send_message(
        chat_id=update.message.chat_id, text=weather_summary
    )


def _humanized_list(items):
    if len(items) == 1:
        return items[0]
    else:
        return ", ".join(items[:1]) + f" & {items[-1]}"


def _get_movement_action():
    return random.choice(
        [
            "take a trip to",
            "head on over to",
            "walk on down to",
            "make a quick jaunt to",
            "find yourself in",
            "ride the bus to",
            "have a nice bike ride over to",
        ]
    )


def bored(update, context):
    first_neighborhood = random.choice(NEIGHBORHOODS)

    restaurant = random.choice(
        yelp.search_query(
            location=first_neighborhood,
            limit=10,
            open_now=True,
            categories="restaurants",
        )["businesses"]
    )

    restaurant_categories = [
        category["title"] for category in restaurant["categories"]
    ]

    second_neighborhood = random.choice(NEIGHBORHOODS)

    bar = random.choice(
        yelp.search_query(
            location=second_neighborhood,
            limit=10,
            open_now=True,
            categories="bars",
        )["businesses"]
    )

    eat_action = random.choice(
        ["grab a bite", "have a snack", "get some grub", "enjoy the nice food"]
    )

    drink_action = random.choice(
        [
            "grab a drink",
            "smash a few whiteclaws",
            "have a cold one",
            "take it easy",
        ]
    )

    message = " ".join(
        [
            f"First, {_get_movement_action()} {first_neighborhood} and",
            f"{eat_action} at {restaurant['name']} ({_humanized_list(restaurant_categories)}).",
            f"Then, {_get_movement_action()} {second_neighborhood} and {drink_action} at {bar['name']}.",
        ]
    )

    context.bot.send_message(chat_id=update.message.chat_id, text=message)


commands = {
    "bored": bored,
    "cat": cat,
    "help": start,
    "hood": hood,
    "joke": joke,
    "start": start,
    "weather": weather,
}

for command_name, command_function in commands.items():
    updater.dispatcher.add_handler(
        CommandHandler(command_name, command_function)
    )

print("listening")
updater.start_polling()
