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

intents = discord.Intents(messages=True, message_content=True)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(
        f'{client.user} logged in\n'
    )

@client.event
async def on_message(message):
    # URL template
    url = 'https://en.wikipedia.org/?curid={pid}'

    # Ignore if message from self
    if message.author == client.user:
        return
    
    # Only respond to messages with command prefix
    if message.content.startswith('wiki!') or message.content.startswith('Wiki!'):
        # Search specific article
        if message.content.split("!", 1)[1].startswith("search"):
            # Search page
            try:
                p = wikipedia.page(message.content[12:])
            # Handle pages requiring disambiguation
            except mediawiki.DisambiguationError as e:
                errMsg = message.content[12:] + " may refer to:\n"
                for o in e.options:
                    errMsg += o + "\n"
                await message.channel.send(errMsg)
                return
            # Handle non existent pages
            except mediawiki.PageError as e:
                await message.channel.send("\"" + message.content[12:] + "\" does not match any pages. Try another query!")
                return
            await message.channel.send(url.format(pid = p.pageid))
            return
        # Search random article
        if message.content.split("!", 1)[1] == "random":
            # Search page
            try:
                p = wikipedia.page(wikipedia.random())
            # Handle pages requiring disambiguation
            except mediawiki.DisambiguationError as e:
                s = random.choice(e.options)
                p = wikipedia.page(s)
            await message.channel.send(url.format(pid = p.pageid))
            return
        # Show commands
        if message.content.split("!", 1)[1] == "help":
            await message.channel.send("Usage:\nwiki!search [Article Name]\nwiki!random")
            return
        # Handle invalid commands
        await message.channel.send("Invalid Command")
    else:
        return

client.run(TOKEN)