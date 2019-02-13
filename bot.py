#!/usr/bin/env python3

from telethon import TelegramClient, sync, events
import time

API_ID = 566798
API_HASH = "f44dfd753ceef8b2676b3f474cf8cc5f"

client = TelegramClient("session", API_ID, API_HASH).start(phone="+1 415 941 9726")

@client.on(events.NewMessage(pattern="hi"))
async def hi(event):
    await event.respond("bot: hey!")

@client.on(events.NewMessage(pattern="pizza"))
async def pizza(event):
    await event.respond("bot: ordering a pizza. please wait...")
    time.sleep(10)
    await event.respond("bot: pizza ordered!")

client.run_until_disconnected()
