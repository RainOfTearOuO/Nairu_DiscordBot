import discord
from discord.ext import commands

import importlib
from .aisrc import aicore
importlib.reload(aicore)

chat_manager = aicore.build_nairu_manager()

class Nairu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._message_filter = {"男娘", "南梁"}
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        
        if message.reference: # user uses reply to answer bot
            try:
                replied_message = await message.channel.fetch_message(message.reference.message_id)
                
                if replied_message.author == self.bot.user:
                    async with message.channel.typing():
                        final_msg = f"{message.author.name}：{message.content}"
                        response = chat_manager.send_to_ai(final_msg, str(message.channel.id))
                        # print(f"finalmsg: {final_msg}")
                        # print(response)

                        for word in self._message_filter:
                            if word in final_msg:
                                await message.reply(f"Filtered.")
                                return
                        await message.reply(f"{response}")
            except Exception as e:
                # print(f"error in AIBehavior: {e}")
                await message.channel.send(f"```{e}```")
        elif self.bot.user.mentioned_in(message): # user mentions bot
            async with message.channel.typing():
                try:
                    msg_without_mention = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
                    final_msg = f"{message.author.name}：{msg_without_mention}"
                    response = chat_manager.send_to_ai(final_msg, str(message.channel.id))
                    # print(f"finalmsg: {final_msg}")
                    # print(response)
                    for word in self._message_filter:
                        if word in final_msg:
                            await message.reply(f"Filtered.")
                            return
                    await message.reply(f"{response}")
                except Exception as e:
                    # print(f"error in AIBehavior: {e}")
                    await message.channel.send(f"```{e}```")
    
    @commands.command()
    async def clear_chat(self, ctx: commands.Context, *, msg = None):
        if chat_manager.clear_channel_chat_history(str(ctx.channel.id)) == True:
            await ctx.send(f"已清除該頻道bot聊天紀錄")
        else:
            await ctx.send(f"bot沒有聊天紀錄可以清除")
    
    @commands.command(help="顯示該頻道的聊天紀錄 (僅限管理者使用)")
    @commands.is_owner()
    async def show_history(self, ctx: commands, *, msg = None):
        history = chat_manager.show_channel_chat_history(str(ctx.channel.id))
        if history == None:
            await ctx.send(f"None")
        else:
            await ctx.send(f"{str(history)}")

        
async def setup(bot):
    await bot.add_cog(Nairu(bot))