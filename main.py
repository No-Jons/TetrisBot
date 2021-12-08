import discord

from discord.ext import commands
from utils.auth import Auth

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.command()
async def test(ctx):
    await ctx.send("works")


if __name__ == '__main__':
    bot.load_extension("cogs.tetris")
    bot.run(Auth.TOKEN)
