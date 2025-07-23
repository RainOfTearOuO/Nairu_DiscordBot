import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._message_filter = {"男娘", "南梁"}
    
    @commands.command()
    async def say(self, ctx: commands.Context, *, msg = None):
        if msg is None:
            async with ctx.channel.typing():
                await ctx.send(f"Usage: {ctx.prefix}say [message]")
        else:
            async with ctx.channel.typing():
                for word in self._message_filter:
                    if word in msg:
                        await ctx.send(f"Filtered.")
                        return
                await ctx.send(msg)
                await ctx.message.delete()



# *** cog load in bot ***   
async def setup(bot):
    await bot.add_cog(Say(bot))