import discord
from discord.ext import commands
import os
from msg_cog import msg_cog 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")
bot.add_cog(msg_cog(bot))


# Run the bot with your Discord token
#token = os.environ.get("DISCORD_TOKEN")
bot.run("MTE3OTEwMTE5MjkxMjExMzc5NA.G7aYLH.M6oryCut75jXg-3DYbPYvARYXXvAjimCfjwxlU")
