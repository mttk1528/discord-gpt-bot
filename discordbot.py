import discord
import openai
import traceback
from discord.ext import commands
from os import getenv

intents = discord.Intents.all()
client = discord.Client(intents=intents)

class ChatGPT:
    def __init__(self, system_setting):
        self.system = {"role": "system", "content": system_setting}
        self.input_list = [self.system]
        self.logs = []

    def input_message(self, input_text):
        self.input_list.append({"role": "user", "content": input_text})
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.input_list
        )
        self.logs.append(result)
        self.input_list.append(
            {"role": "assistant", "content": result.choices[0].message.content}
        )
        
@client.event
async def on_ready():
    print("activated")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!gpt'):
        question = message.content[4:]
        api = ChatGPT(system_setting="You should act as an assistant. Conversation starting now")
        api.input_message(question)
        answer = api.input_list[-1]["content"]
        await message.channel.send(answer)


openai.api_key = getenv('OPENAI_API_TOKEN')
token = getenv('DISCORD_BOT_TOKEN')
client.run(token)

