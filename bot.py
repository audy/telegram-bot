#!/usr/bin/env python3

from telethon import TelegramClient, sync, events
import re
import random
import time
import requests

from neighborhoods import NEIGHBORHOODS

API_ID = 771357
API_HASH = "696dba4ddacd457a72fc8317b9f01866"

# thecatapi.com
CAT_API_KEY = "9f053a85-ef38-470b-914e-d1c3bffafd65"


client = TelegramClient("session", API_ID, API_HASH).start(phone="+1 352 200 2839")


def get_random_joke():
    resp = requests.get(
        "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
    )
    return resp.json()["joke"]


def get_random_cat():
    resp = requests.get("https://api.thecatapi.com/v1/images/search?size=full")
    return resp.json()[0]["url"]


print("---> running")


@client.on(events.NewMessage(pattern=re.compile(r"cat", re.IGNORECASE)))
async def cat(event):
    await event.respond(get_random_cat())


@client.on(events.NewMessage(pattern=re.compile(r"joke", re.IGNORECASE)))
async def joke(event):
    await event.respond(get_random_joke())


@client.on(events.NewMessage(pattern=re.compile(r"hi", re.IGNORECASE)))
async def hi(event):
    greetings = ["Hello!", "Sup?", "Hi!", "Hallo", "¡Hola!"]
    await event.respond(random.choice(greetings))


@client.on(events.NewMessage(pattern=re.compile(r"Bye", re.IGNORECASE)))
async def bye(event):
    greetings = ["Bye.", "oh wow!", "FINE", "Goodbye", "Love You"]
    await event.respond(random.choice(greetings))


@client.on(events.NewMessage(pattern=re.compile(r"hood", re.IGNORECASE)))
async def hood(event):
    await event.respond(random.choice(NEIGHBORHOODS))

client.run_until_disconnected()
