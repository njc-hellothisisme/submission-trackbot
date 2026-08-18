# This example requires the 'message_content' intent.
import os
import discord
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("token")
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot is ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token)