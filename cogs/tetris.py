import discord
import asyncio

from discord.ext import commands
from utils.tetris import Game

PIECE_DISPLAYS = {
    "l1": "⬛⬛⬛⬛\n⬛🟧⬛⬛\n⬛🟧⬛⬛\n⬛🟧🟧⬛\n⬛⬛⬛⬛",
    "l2": "⬛⬛⬛⬛\n⬛⬛🟦⬛\n⬛⬛🟦⬛\n⬛🟦🟦⬛\n⬛⬛⬛⬛",
    "line": "⬛⬛⬛\n⬛🟨⬛\n⬛🟨⬛\n⬛🟨⬛\n⬛🟨⬛\n⬛⬛⬛",
    "t": "⬛⬛⬛⬛⬛\n⬛🟪🟪🟪⬛\n⬛⬛🟪⬛⬛\n⬛⬛⬛⬛⬛",
    "square": "⬛⬛⬛⬛\n⬛🟥🟥⬛\n⬛🟥🟥⬛\n⬛⬛⬛⬛",
    "s1": "⬛⬛⬛⬛\n⬛🟩⬛⬛\n⬛🟩🟩⬛\n⬛⬛🟩⬛\n⬛⬛⬛⬛",
    "s2": "⬛⬛⬛⬛\n⬛⬛🟫⬛\n⬛🟫🟫⬛\n⬛🟫⬛⬛\n⬛⬛⬛⬛"
}

PIECE_DISPLAYS_M = {
    "l1": "⬛⬛⬛⬛\n⬛⬜⬛⬛\n⬛⬜⬛⬛\n⬛⬜⬜⬛\n⬛⬛⬛⬛",
    "l2": "⬛⬛⬛⬛\n⬛⬛⬜⬛\n⬛⬛⬜⬛\n⬛⬜⬜⬛\n⬛⬛⬛⬛",
    "line": "⬛⬛⬛\n⬛⬜⬛\n⬛⬜⬛\n⬛⬜⬛\n⬛⬜⬛\n⬛⬛⬛",
    "t": "⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬛\n⬛⬛⬜⬛⬛\n⬛⬛⬛⬛⬛",
    "square": "⬛⬛⬛⬛\n⬛⬜⬜⬛\n⬛⬜⬜⬛\n⬛⬛⬛⬛",
    "s1": "⬛⬛⬛⬛\n⬛⬜⬛⬛\n⬛⬜⬜⬛\n⬛⬛⬜⬛\n⬛⬛⬛⬛",
    "s2": "⬛⬛⬛⬛\n⬛⬛⬜⬛\n⬛⬜⬜⬛\n⬛⬜⬛⬛\n⬛⬛⬛⬛"
}


class Tetris(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = dict()
        self.channels = list()
        self.users = list()
        self.reactions = ("⬅️", "➡️", "⬇️", "↩️")

    @commands.command(aliases=["play", "tetris"])
    async def start(self, ctx, monochrome: bool = None):
        if ctx.channel.id in self.channels:
            return await ctx.send("There's already a game in this channel!")
        if ctx.author.id in self.users and not ctx.author.id == 448250281097035777:
            return await ctx.send("You already have an active game running!")
        if not monochrome:
            monochrome = ctx.author.is_on_mobile()
        game = Game(monochrome=monochrome)
        m = await ctx.send(embed=self._render_embed(game))
        self.games[ctx.author.id] = {"game": game, "message": m}
        self.channels.append(ctx.channel.id)
        self.users.append(ctx.author.id)
        for emoji in self.reactions:
            await m.add_reaction(emoji)
        while self.games.get(ctx.author.id):
            await asyncio.sleep(1)
            loss = game.increment()
            if loss:
                del self.games[ctx.author.id]
                self.channels.remove(ctx.channel.id)
                self.users.remove(ctx.author.id)
                await m.edit(embed=self._render_embed(game, loss=loss))
            else:
                await m.edit(embed=self._render_embed(game))
        await ctx.send(f"Game over!\nLines: {game.lines}")

    @staticmethod
    def _render_embed(game, loss: bool = False):
        embed = discord.Embed(title="Tetris" if not loss else "Game over!", color=discord.Color.dark_blue())
        embed.add_field(name="_ _", value=game.render())
        if game.monochrome:
            embed.add_field(name="Next:",
                            value="```" + PIECE_DISPLAYS_M[game.next_piece["id"].replace("a_", "")] + "```")
        else:
            embed.add_field(name="Next:", value="```" + PIECE_DISPLAYS[game.next_piece["id"].replace("a_", "")] + "```")
        embed.add_field(name="Lines:", value=game.lines, inline=False)
        return embed

    @commands.command(aliases=["stop"])
    async def end(self, ctx):
        if ctx.author.id not in self.users or ctx.channel.id not in self.channels:
            return
        del self.games[ctx.author.id]
        self.channels.remove(ctx.channel.id)
        self.users.remove(ctx.author.id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id == self.bot.user.id:
            return
        entry = self.games.get(payload.member.id)
        if not entry:
            return
        entry["game"].do_action(str(payload.emoji))


def setup(bot):
    bot.add_cog(Tetris(bot))
