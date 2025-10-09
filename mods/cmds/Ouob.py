import discord
import os
from discord.ext import commands

class Ouob(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ouob_image_path = "images/ouob.png"
        self.base_path = os.path.dirname(__file__)

    @commands.command()
    async def ouob(self, ctx: commands.Context):
        try:
            img_path = os.path.join(self.base_path, self.ouob_image_path)
            picture = discord.File(img_path)
            async with ctx.typing():
                await ctx.send(file = picture)
        except Exception as e:
            print(f"[ouob] Error: {e}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.mentions or message.content.startswith(self.bot.command_prefix):
            return
        
        if "ouob" == message.content.lower():
            try:
                img_path = os.path.join(self.base_path, self.ouob_image_path)
                picture = discord.File(img_path)
                async with message.channel.typing():
                    await message.channel.send(file = picture)
            except Exception as e:
                print(f"[ouob] Error: {e}")

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Ouob(bot))