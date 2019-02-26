#!/usr/bin/env python3

from icalevents import icalevents as ical

from telethon import TelegramClient, sync, events
import requests

from neighborhoods import NEIGHBORHOODS

import re
import random
import time
import datetime


API_ID = 771_357
API_HASH = "696dba4ddacd457a72fc8317b9f01866"

# thecatapi.com
CAT_API_KEY = "9f053a85-ef38-470b-914e-d1c3bffafd65"


client = TelegramClient("session", API_ID, API_HASH).start(phone="+1 352 200 2839")


def get_gym_events():
    GYM_URL = "http://touchstoneclimbing.time.ly/?plugin=all-in-one-event-calendar&controller=ai1ec_exporter_controller&action=export_events&no_html=true&ai1ec_tag_ids=31&&"
    events = ical.events(
        GYM_URL,
        start=datetime.date.today(),
        end=datetime.date.today() + datetime.timedelta(days=1),
    )

    event_message = []

    for event in events:
        start = event.start.strftime("%a (%d/%-m) %I:%M %p")
        end = event.end.strftime("%I:%M %p")
        event_message.append(f"* {start} - {end}: {event.summary}")
    return "\n".join(event_message)


def get_weather_summary():
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

    return weather_summary


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


@client.on(events.NewMessage(pattern=re.compile(r"weather", re.IGNORECASE)))
async def weather(event):
    weather_summary = get_weather_summary()
    await event.respond(weather_summary)


@client.on(events.NewMessage(pattern=re.compile(r"gym", re.IGNORECASE)))
async def gym(event):
    await event.respond(get_gym_events())


client.run_until_disconnected()
