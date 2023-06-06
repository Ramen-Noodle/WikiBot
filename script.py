# bot.py
import os

import random

import mediawiki
from mediawiki import MediaWiki

wikipedia = MediaWiki()

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents(messages=True, message_content=True)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

@client.event
async def on_message(message):
    url = 'https://en.wikipedia.org/?curid={pid}'
    if message.author == client.user:
        return
    
    if message.content.startswith('wiki!'):
        if message.content.split("!", 1)[1].startswith("search"):
            try:
                p = wikipedia.page(message.content[12:])
            except mediawiki.DisambiguationError as e:
                errMsg = message.content[12:] + " may refer to:\n"
                for o in e.options:
                    errMsg += o + "\n"
                await message.channel.send(errMsg)
                return
            except mediawiki.PageError as e:
                await message.channel.send("\"" + message.content[12:] + "\" does not match any pages. Try another query!")
                return
            await message.channel.send(url.format(pid = p.pageid))
            return
        if message.content.split("!", 1)[1] == "random":
            try:
                p = wikipedia.page(wikipedia.random())
            except mediawiki.DisambiguationError as e:
                s = random.choice(e.options)
                p = wikipedia.page(s)
            await message.channel.send(url.format(pid = p.pageid))
            return
        await message.channel.send("Invalid Command")
    else:
        return

client.run(TOKEN)