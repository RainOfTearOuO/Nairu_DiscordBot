import discord
import asyncio
from discord.ext import commands

class TestException(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return f"TestException: {self.message}"

class TestExcept(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def test_except(self, ctx):
        try:
            raise TestException("This is a test exception.")
        except TestException as e:
            raise e
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.content.startswith(self.bot.command_prefix):
            return
        
        try:
            if "test_on_message_error" in message.content.lower():
                raise TestException("Triggered by message content.")
        except TestException as e:
            raise e
        
        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(TestExcept(bot))