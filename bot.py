import os
import asyncio
import discord
import signal
import sys
from aiohttp import web
import threading
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
shutdown_flag = False

# *** Load config and main function ***
TOKEN = os.environ.get("TOKEN")
MODS_FOLDER = os.environ.get("MODS_FOLDER")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='nr!', intents = intents)

@bot.event
async def on_ready():
    print(f"Current Login Identity --> {bot.user}")

# 載入指令程式檔案
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"{MODS_FOLDER}.{extension}")
    await ctx.send(f"Loaded {MODS_FOLDER}.{extension} done.")

# 卸載指令檔案
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"{MODS_FOLDER}.{extension}")
    await ctx.send(f"UnLoaded {MODS_FOLDER}.{extension} done.")

# 重新載入程式檔案
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"{MODS_FOLDER}.{extension}")
    await ctx.send(f"ReLoaded {MODS_FOLDER}.{extension} done.")

# all mod folder
@bot.command(help="顯示所有在模組資料夾裡面的檔案 (僅限擁有者使用)")
@commands.is_owner()
async def showmodfolder(ctx, *, msg = ""):
    modFolderList = os.listdir(f"./{MODS_FOLDER}")
    content = ""
    for modType in modFolderList:
        mod_path = f"./{MODS_FOLDER}/{modType}"
        py_files = [f for f in os.listdir(mod_path) if f.endswith(".py")]
        # if not py_files and msg == "":
        #     continue

        content += f"{modType}:\n"
        for file in py_files:
            content += f"\t\t{file[:-3]}\n"
        content += "\n"

    await ctx.send(content)

# show loaded mods
@bot.command(help="顯示已載入的模組")
async def showloadedmods(ctx):
    extensionList = list(bot.extensions.keys())
    if not extensionList:
        await ctx.send(f"None")
    else:
        await ctx.send(f"Loaded mods:\n{extensionList}")

@bot.command(help="關閉 bot (僅限擁有者使用)")
@commands.is_owner()
async def shutdown(ctx):
    # global shutdown_flag
    # if shutdown_flag:
        await ctx.send("機器人關閉中...")
        await bot.close()
    
    # else:
    #     shutdown_flag = True
    #     await ctx.send("⚠️請在 10 秒內再次輸入 `nr!shutdown` 確認！")
    #     try:
    #         await asyncio.sleep(10)
    #     finally:
    #         shutdown_flag = False

@bot.event  
async def on_command_error(ctx, error):
    await ctx.send(f"**command ERROR**: \n{error}")

@bot.event
async def on_error(event, *args, **kwargs):
    print(event)

# load all extensions (only use while start bot.py)
async def load_extensions(): 
    for packageFolder in os.listdir(f"./{MODS_FOLDER}"):
        for filename in os.listdir(f"./{MODS_FOLDER}/{packageFolder}"):
            if filename.endswith(".py"):
                await bot.load_extension(f"{MODS_FOLDER}.{packageFolder}.{filename[:-3]}")

async def handle(request):
    return web.Response(text="Bot is alive.")

async def run_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = 10000
    site = web.TCPSite(runner, port=port)
    await site.start()
    print(f"Web server running on port {port}")

def signal_handler(sig, frame):
    print("已按下Ctrl+C，關閉Bot...")
    loop = asyncio.get_event_loop()
    # 在 event loop 裡排程非同步關閉任務
    loop.create_task(bot.close())

async def main():
    await run_web_server()
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    asyncio.run(main())