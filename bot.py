#!/usr/bin/env python3

from telethon import TelegramClient, sync, events
import re
import random
import time

API_ID = 771357
API_HASH = "696dba4ddacd457a72fc8317b9f01866"

client = TelegramClient("session", API_ID, API_HASH).start(phone="+1 352 200 2839")


print("---> running")


@client.on(events.NewMessage(pattern=re.compile(r"hi", re.IGNORECASE)))
async def hi(event):
    greetings = ["Hello!", "Sup?", "Hi!", "Hallo", "¡Hola!"]
    await event.respond(random.choice(greetings))

 @client.on(events.NewMessage(pattern=re.compile(r"hi", re.IGNORECASE)))
async def bye(event):
    greetings = ["Bye.", "oh wow!", "FINE", "Good Bye", "Love You"]
    await event.respond(random.choice(greetings))

client.run_until_disconnected()
