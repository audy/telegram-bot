#!/usr/bin/env python3

import logging
import os
import random

import requests
from telegram.ext import CommandHandler, Updater
from yelpapi import YelpAPI

from neighborhoods import NEIGHBORHOODS


class Keys:
    @classmethod
    def get_yelp(_):
        return os.environ["YELP_API_KEY"]

    @classmethod
    def get_telegram(_):
        return os.environ["TELEGRAM_API_KEY"]

    @classmethod
    def get_darksky(_):
        return os.environ["DARKSKY_API_KEY"]


YELP = YelpAPI(Keys.get_yelp())


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
    resp = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
    joke = resp.json()["joke"]
    context.bot.send_message(chat_id=update.message.chat_id, text=joke)


def weather(update, context):
    resp = requests.get(f"https://api.darksky.net/forecast/{Keys.get_darksky()}/37.8267,-122.4233")

    weather_data = resp.json()

    weather_summary = f"""
Currently: {weather_data['minutely']['summary']}
(Wind={weather_data['currently']['windSpeed']}-mph; Temp={weather_data['currently']['temperature']}-F Humidity={100*weather_data['currently']['humidity']}%)
Today: {weather_data['hourly']['summary']}
Forecast: {weather_data['daily']['summary']}
"""

    context.bot.send_message(chat_id=update.message.chat_id, text=weather_summary)


def rona_bored(update, context):
    """ replacement for /bored during social-distancing """
    eat_action = random.choice(
        ["grab a bite", "have a snack", "get some grub", "enjoy the nice food"]
    )

    rooms = ["living room", "bedroom", "office", "closet", "garage", "bathroom", "kitchen"]

    drink_action = random.choice(
        ["grab a drink", "smash a few whiteclaws", "have a cold one", "take it easy"]
    )

    message = " ".join(
        [
            f"First, {_get_movement_action()} {random.choice(rooms)} and",
            f"{eat_action} at {random.choice(rooms)} (kitchen).",
            f"Then, {_get_movement_action()} {random.choice(rooms)} and {drink_action} at {random.choice(rooms)}.",
        ]
    )

    context.bot.send_message(chat_id=update.message.chat_id, text=message)


def _humanized_list(items):
    """convert a list of items into something that could go into an English sentence"""
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


def delivery(update, context):
    """ random food delivery. Useful for #TakeoutTuesday """
    first_neighborhood = random.choice(NEIGHBORHOODS)

    # I guess every restaurant that is open now probably delivers :shrug:
    restaurant = random.choice(
        YELP.search_query(
            location=first_neighborhood, limit=10, open_now=True, categories="restaurants"
        )["businesses"]
    )

    action = random.choice(
        [
            "crack open a cold one",
            "turn on netflix",
            "take a bath with a friend",
            "do some social distancing",
            "work on yours crafts project",
            "zoom your relatives",
            "zoom your friends",
            "zoom your Grindr match",
            "zoom your Hinge match",
            "read a book",
            "stare at the ceiling",
            "give yourself a haircut",
            "do some exercise",
            "stare out the window",
            "earn some fortnite frags",
            "study some speedruns",
        ]
    )

    restaurant_categories = [category["title"] for category in restaurant["categories"]]

    message = " ".join(
        [
            action,
            f"and order delivery from {restaurant['name']} ({_humanized_list(restaurant_categories)})",
            restaurant["url"].split("?")[0],
        ]
    )

    context.bot.send_message(chat_id=update.message.chat_id, text=message)


def bored(update, context):
    """ Suggest something to do on a Saturday """
    first_neighborhood = random.choice(NEIGHBORHOODS)

    restaurant = random.choice(
        YELP.search_query(
            location=first_neighborhood, limit=10, open_now=True, categories="restaurants"
        )["businesses"]
    )

    restaurant_categories = [category["title"] for category in restaurant["categories"]]

    second_neighborhood = random.choice(NEIGHBORHOODS)

    bar = random.choice(
        YELP.search_query(location=second_neighborhood, limit=10, open_now=True, categories="bars")[
            "businesses"
        ]
    )

    eat_action = random.choice(
        ["grab a bite", "have a snack", "get some grub", "enjoy the nice food"]
    )

    drink_action = random.choice(
        ["grab a drink", "smash a few whiteclaws", "have a cold one", "take it easy"]
    )

    message = " ".join(
        [
            f"First, {_get_movement_action()} {first_neighborhood} and",
            f"{eat_action} at {restaurant['name']} ({_humanized_list(restaurant_categories)}).",
            f"Then, {_get_movement_action()} {second_neighborhood} and {drink_action} at {bar['name']}.",
        ]
    )

    context.bot.send_message(chat_id=update.message.chat_id, text=message)


def main():

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    updater = Updater(token=Keys.get_telegram(), use_context=True)

    commands = {
        "bored": rona_bored,
        "cat": cat,
        "help": start,
        "hood": hood,
        "joke": joke,
        "start": start,
        "weather": weather,
        "delivery": delivery,
    }

    for command_name, command_function in commands.items():
        updater.dispatcher.add_handler(CommandHandler(command_name, command_function))

    print("listening")
    updater.start_polling()


if __name__ == "__main__":
    main()
