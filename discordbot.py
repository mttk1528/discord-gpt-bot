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
    {"role": "user", "content": "Hello. Please introduce yourself."},
    {"role": "assistant", "content": "I am ChatGPT. How can I help you?"}
]

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)



token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

