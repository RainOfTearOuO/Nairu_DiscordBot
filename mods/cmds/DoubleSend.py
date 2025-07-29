import discord
import asyncio
from discord.ext import commands

class FilteredWordError(Exception):
    def __init__(self, word):
        self.word = word
    
    def __str__(self):
        return f"Filtered word detected: {self.word}"

class DoubleSend(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lastChannelSentMessage = {}
        self._message_filter = {"男娘","南梁"}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.mentions or message.content.startswith(self.bot.command_prefix):
            return
        
        channel_id = str(message.channel.id)
        
        try:
            if channel_id not in self.lastChannelSentMessage:
                # no channel history
                self.lastChannelSentMessage[channel_id] = message.content
            elif not self.lastChannelSentMessage[channel_id] or self.lastChannelSentMessage[channel_id] != message.content:
                # has channel history and message is different
                self.lastChannelSentMessage[channel_id] = message.content
            else:
                async with message.channel.typing():
                    for word in self._message_filter:
                        if word in message.content:
                            await asyncio.sleep(1)
                            await message.channel.send(f"Filtered.")
                            raise FilteredWordError(word)
                    await asyncio.sleep(1)
                    await message.channel.send(f"{message.content}")

        except FilteredWordError as e:
            print(f"[DoubleSend] FilteredWordError: {e}")

        except discord.HTTPException as e:
            print(f"[DoubleSend] discord.HTTPException: {e}")

        except Exception as e:
            print(f"[DoubleSend] Exception: {e}")
            await asyncio.sleep(1)
            await message.channel.send(f"```{e}```")

        await self.bot.process_commands(message)

# *** cog load in bot ***
async def setup(bot):
    await bot.add_cog(DoubleSend(bot))