import discord
from discord.ext import commands
from responses import process_question, lore_data

# Set up the intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True 

# Initialize the bot with the command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command(name='ask')
async def ask(ctx, *, question):
    # Process the question
    response = process_question(question, lore_data)
    await ctx.send(response)
