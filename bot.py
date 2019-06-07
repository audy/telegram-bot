#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler

import re
import random
import time
import requests
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

updater = Updater(
    token="636614158:AAEDn80O9QQyOq5PW1a8lk1Yb2SUhBlny2I", use_context=True
)


def joke(update, context):
    resp = requests.get(
        "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
    )
    joke = resp.json()["joke"]
    context.bot.send_message(chat_id=update.message.chat_id, text=joke)


def cat(update, context):
    resp = requests.get("https://api.thecatapi.com/v1/images/search?size=full")
    cat_url = resp.json()[0]["url"]
    context.bot.send_message(chat_id=update.message.chat_id, text=cat_url)


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, text="I'm a bot, please talk to me!"
    )


start_handler = CommandHandler("start", start)
updater.dispatcher.add_handler(start_handler)

cat_handler = CommandHandler("cat", cat)
updater.dispatcher.add_handler(cat_handler)

updater.start_polling()
