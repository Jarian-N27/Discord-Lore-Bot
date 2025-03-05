from bot import bot
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Run the bot
if __name__ == '__main__':
    bot.run(TOKEN)
