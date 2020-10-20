#!/usr/bin/env python3

import logging
import os
import random

import requests
from telegram.ext import CommandHandler, Updater
from yelpapi import YelpAPI

from neighborhoods import NEIGHBORHOODS

import helpers


class Keys:
    """ keys for various external services """

    @classmethod
    def get_yelp(_):
        return os.environ["YELP_API_KEY"]

    @classmethod
    def get_darksky(_):
        return os.environ["DARKSKY_API_KEY"]


YELP = YelpAPI(Keys.get_yelp())


class Bot:
    def __init__(self):
        self.telegram_api_key = os.environ["TELEGRAM_API_KEY"]
        self.updater = Updater(token=self.telegram_api_key, use_context=True)

        # trigger -> handler function
        self.handlers = {}

    def start(self):
        self._register_handlers()
        self.updater.start_polling()

    def help(self):
        """ auto-generated handler for /help """
        return " ".join([f"/{k}" for k in self.handlers.keys()])

    def _register_handlers(self):
        self.responds_to("help")(self.help)

        for command_name, command_function in self.handlers.items():
            print(f"registered: {command_name} {command_function}")
            self.updater.dispatcher.add_handler(
                CommandHandler(command_name, self._handler_wrapper(command_function))
            )

    def _handler_wrapper(self, handler_function):
        return lambda update, context: context.bot.send_message(
            chat_id=update.message.chat_id, text=handler_function()
        )

    def responds_to(self, trigger):
        def wrapper(handler):
            assert trigger not in self.handlers, f"duplicated trigger! {trigger} -> {handler}"
            self.handlers[trigger] = handler
            return handler

        return wrapper


bot = Bot()


@bot.responds_to("cat")
def cat():
    """ a random cat photo """
    resp = requests.get("https://api.thecatapi.com/v1/images/search?size=full")
    return resp.json()[0]["url"]

@bot.responds_to("dog")
def dog():
    """ a random dog photo"""
    resp = requests.get("https://api.thedogapi.com/v1/images/search?size=full")
    return resp.json()[0]["url"]


@bot.responds_to("hood")
def hood():
    """ a random neighborhood in SF """
    return random.choice(NEIGHBORHOODS)


@bot.responds_to("joke")
def joke():
    """ tell a joke """
    resp = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
    return resp.json()["joke"]


@bot.responds_to("weather")
def weather():
    resp = requests.get(f"https://api.darksky.net/forecast/{Keys.get_darksky()}/37.8267,-122.4233")

    weather_data = resp.json()
    # TODO: left pad
    return f"""
Currently: {weather_data['minutely']['summary']}
(Wind={weather_data['currently']['windSpeed']}-mph; Temp={weather_data['currently']['temperature']}-F Humidity={100*weather_data['currently']['humidity']}%)
Today: {weather_data['hourly']['summary']}
Forecast: {weather_data['daily']['summary']}
"""


@bot.responds_to("bored")
def rona_bored():
    """ replacement for /bored during social-distancing """
    eat_action = random.choice(
        ["grab a bite", "have a snack", "get some grub", "enjoy the nice food"]
    )

    rooms = ["living room", "bedroom", "office", "closet", "garage", "bathroom", "kitchen"]

    drink_action = random.choice(
        ["grab a drink", "smash a few whiteclaws", "have a cold one", "take it easy"]
    )

    return " ".join(
        [
            f"First, {helpers.get_movement_action()} {random.choice(rooms)} and",
            f"{eat_action} at {random.choice(rooms)} (kitchen).",
            f"Then, {helpers.get_movement_action()} {random.choice(rooms)} and {drink_action} at {random.choice(rooms)}.",
        ]
    )


@bot.responds_to("delivery")
def delivery():
    """ random food delivery. Useful for #TakeoutTuesday """
    first_neighborhood = random.choice(NEIGHBORHOODS)

    # I guess every restaurant that is open now probably delivers :shrug:
    restaurant = random.choice(
        YELP.search_query(
            location=f"{first_neighborhood}, San Francisco, CA", limit=10, open_now=True, categories="restaurants"
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

    return " ".join(
        [
            action,
            f"and order delivery from {restaurant['name']} ({helpers.humanized_list(restaurant_categories)}) in the {first_neighborhood}",
            restaurant["url"].split("?")[0],
        ]
    )


@bot.responds_to("og_bored")
def bored():
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
        ["grab a bite", "have a snack", "get some grub", "enjoy the nice food", "munch on some tasties"]
    )

    drink_action = random.choice(
        ["grab a drink", "smash a few whiteclaws", "have a cold one", "take it easy", "toss a few dice"]
    )

    return " ".join(
        [
            f"First, {helpers.get_movement_action()} {first_neighborhood} and",
            f"{eat_action} at {restaurant['name']} ({helpers.humanized_list(restaurant_categories)}).",
            f"Then, {helpers.get_movement_action()} {second_neighborhood} and {drink_action} at {bar['name']}.",
        ]
    )


@bot.responds_to("hello")
def hello():
    """ returns a greeting """
    return random.choice(["Hola", "Hallo", "Hello", "Salut", "Ola", "Labas", "Sawubona", "Talofa"])


@bot.responds_to("dogfact")
def dogfact():
    return requests.get("http://dog-api.kinduff.com/api/facts").json()["facts"][0]


@bot.responds_to("catfact")
def catfact():
    """
    Get a random cat fact from catfact.jinja
    """
    return requests.get("https://catfact.ninja/fact").json()["fact"]


@bot.responds_to("trivia")
def trivia():
    trivia = requests.get("https://opentdb.com/api.php?amount=1").json()
    result = trivia["results"][0]
    return result["question"]


@bot.responds_to("potato")
def potato():
    if random.randint(0,100) < 33:
        return "tomato"
    return " ".join(["potato" for _ in range(0, random.randint(0, 10))])


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    print("listening!")
    bot.start()


if __name__ == "__main__":
    main()
