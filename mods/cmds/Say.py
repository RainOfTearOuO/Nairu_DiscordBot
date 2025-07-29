import discord
from discord.ext import commands

class FilteredWordError(Exception):
    def __init__(self, word):
        self.word = word
    
    def __str__(self):
        return f"Filtered word detected: {self.word}"

class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._message_filter = {"男娘", "南梁"}
    
    @commands.command()
    async def say(self, ctx: commands.Context, *, msg = None):
        try:
            if msg is None:
                async with ctx.channel.typing():
                    await ctx.send(f"Usage: {ctx.prefix}say [message]")
            else:
                async with ctx.channel.typing():
                    for word in self._message_filter:
                        if word in msg:
                            await ctx.send(f"Filtered.")
                            raise FilteredWordError(word)
                    await ctx.send(msg)
                    await ctx.message.delete()
        except FilteredWordError as e:
            print(f"[Say] FilteredWordError: {e}")


# *** cog load in bot ***   
async def setup(bot):
    await bot.add_cog(Say(bot))