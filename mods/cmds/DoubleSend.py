import discord
from discord.ext import commands

class DoubleSend(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lastChannelSentMessage = {}
        self._message_filter = {"男娘","南梁"}
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        prefix = await self.bot.get_prefix(message)
        channel_id = str(message.channel.id)
        if message.content.startswith(prefix) or self.bot.user.mentioned_in(message):
            return
        
        for word in self._message_filter:
            if word in message.content:
                return
        if channel_id not in self.lastChannelSentMessage:
            # no channel history
            self.lastChannelSentMessage[channel_id] = message.content
        elif not self.lastChannelSentMessage[channel_id] or self.lastChannelSentMessage[channel_id] != message.content:
            # has channel history and message is different
            self.lastChannelSentMessage[channel_id] = message.content
        else:
            async with message.channel.typing():
                await message.channel.send(f"{message.content}")
        
        await self.bot.process_commands(message)

# *** cog load in bot ***
async def setup(bot):
    await bot.add_cog(DoubleSend(bot))