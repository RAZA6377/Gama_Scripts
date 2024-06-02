import discord
from discord.ext import commands, tasks
import asyncio
from threading import Thread
import babase as ba
import bascenev1 as bs
from babase._general import Call
import _babase as _ba
import datafiles.bottoken as bt
import json
from colorama import Fore

bot_msg = []
file_path = ba.env()["python_directory_user"] + "/logs/chat.log"
player_path = ba.env()["python_directory_user"] + "/logs/players.log"

# Must Enter These
logschannel = 1234567890
guild_id = 1234567890
prefix = "e!"
server_name = "|| GAMA EPIC PRIVATE ||"
discord_server_name = "Eigen.GAMA"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(Fore.RED + "*****BOT IS ONLINE*****")
    channel = bot.get_channel(logschannel)
    try:
        await channel.purge(limit=100)
        message = await channel.send("Server Live Stats")
        bot_msg.append(message.id)
        print(bot_msg)
        update_message_task.start()
    except Exception as e:
        print(e)

async def read_data_from_file():
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        if not lines:
            return "Empty"
        if len(lines) > 40:
            return "".join(lines[-10:])
        else:
            return "".join(lines)
    except FileNotFoundError:
        return "File not found"

async def players():
    try:
        with open(player_path, "r") as file:
            data = file.read()
        if data == "":
            return "Empty"
        else:
            return data
    except FileNotFoundError:
        return "File not found"

async def update_message():
    try:
        data = await read_data_from_file()
        player = await players()
        guild = bot.get_guild(1050804096388579380)
        channel = bot.get_channel(1233132366978089151)
        msgid = bot_msg[-1]
        message = await channel.fetch_message(msgid)
        embed = discord.Embed(title=f"`{server_name}`", description=f"**Live Players**```{player}```", color=0xA020F0)
        embed.add_field(name="Live Chat", value=f"```{data}```")
        embed.set_footer(text=discord_server_name, icon_url=bot.user.avatar.url)
        embed.set_author(name=discord_server_name, icon_url=guild.icon.url)
        await message.edit(content=None, embed=embed)
    except Exception as e:
        print(e)

@tasks.loop(seconds=5)
async def update_message_task():
    await update_message()

@update_message_task.before_loop
async def before_update_message_task():
    await bot.wait_until_ready()

# Commands
@bot.command()
@commands.has_permissions(administrator=True)
async def send(ctx, *, message: str):
    try:
        
        _ba.pushcall(Call(bs.chatmessage, message), from_other_thread=True)
        msg = ctx.message
        await msg.add_reaction("✔️")
    except Exception as e:
        msg = ctx.message
        await msg.add_reaction("❌")
        print(e)

@bot.command()
@commands.has_permissions(administrator=True)
async def mp(ctx, maxplayers: int):
    try:
        _ba.pushcall(Call(bs.getsession().max_players, maxplayers), from_other_thread=True)
        _ba.pushcall(Call(bs.set_public_party_max_size, maxplayers), from_other_thread=True)
        bs.broadcastmessage(f"Set Maxplayer Limit To {maxplayers}", color=(1, 0, 1))
        await ctx.send(f"Set Maxplayer Size To {maxplayers}")
    except Exception as e:
        print(e)

# Running the bot
tokn = bt.token

async def start_bot():
    await bot.start(tokn)

def run_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def run():
    loop = asyncio.new_event_loop()
    Thread(target=run_thread, args=(loop,)).start()
    asyncio.run_coroutine_threadsafe(start_bot(), loop)

