import discord
import openai
import traceback
from discord.ext import commands
from os import getenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "こんにちは。あなたは誰ですか？"},
    {"role": "assistant", "content": "私は AI アシスタントの AI Qiitan です。なにかお手伝いできることはありますか？"}
]

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!gpt'):
        print(message.content)
        print(message.content.split('>')[1].lstrip())
        messages.append({"role": "user", "content": message.content.split('>')[1].lstrip()})

        openai_api_key = getenv('OPENAI_API_KEY')
        openai.api_key = openai_api_key

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        print(completion.choices[0].message.content)
        await message.channel.send(completion.choices[0].message.content)

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

