#!/usr/bin/env python3

from telethon import TelegramClient, sync, events

API_ID = 566798
API_HASH = "f44dfd753ceef8b2676b3f474cf8cc5f"

client = TelegramClient("session", API_ID, API_HASH).start(phone="+1 415 941 9726")

print(client.get_me().stringify())

@client.on(events.NewMessage(pattern="hi"))
async def hander(event):
    print(event)
    await event.respond("bot: hey!")

client.run_until_disconnected()
