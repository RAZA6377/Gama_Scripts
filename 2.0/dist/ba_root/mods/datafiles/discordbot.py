# Made By RaZa

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
import datetime
import time
import io
import textwrap
from contextlib import redirect_stdout
import traceback
import jishaku
from discord.ui import View, Button

log_msg = []
bot_msg = []
file_path = ba.env()["python_directory_user"] + "/logs/chat.log"
player_path = ba.env()["python_directory_user"] + "/logs/players.log"
logs_path = ba.env()["python_directory_user"] + "/logs/server.log"
staff_file = ba.env()["python_directory_user"] + "/datafiles/staff.json"
f = open(staff_file, "r")
data = json.load(f)
f.close()

# Must Enter These
msgchannel = 1234567890
logschannel = 1234567890
guild_id = 1234567890
prefix = "e!"
server_name = "|| GAMA EPIC PRIVATE ||"
discord_server_name = "Eigen.GAMA"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents, owner_id=924617239301324856)

@bot.event
async def on_ready():
    print(Fore.RED + "*****BOT IS ONLINE*****")
    global msgchannel
    global logschannel
    global guild_id
    channel = bot.get_channel(msgchannel)
    logchannel = bot.get_channel(logschannel)
    try:
        await channel.purge(limit=100)
        await logchannel.purge(limit=100)
        message = await channel.send("Server Live Stats")
        logmsg = await logchannel.send("Server Logs")
        log_msg.append(logmsg.id)
        bot_msg.append(message.id)
        print(bot_msg)
        update_message_task.start()
        serverlog.start()
        await bot.load_extension("jishaku")
    except Exception as e:
        print(e)

def check():

    def pred(ctx):

        try:
            global data

            if int(ctx.author.id) in data["discordstaff"]["userids"]:

                return True

            return False

        except Exception as e:
            print(e)
            pass
    return commands.check(pred)
    

@bot.command()
@commands.is_owner()
async def dcadmin(ctx, member: discord.Member, action: str):
    try:
        if action == "add":
            if int(member.id) in data["discordstaff"]["userids"]:
                await ctx.send("User Is Already An Admin")
            else:
                data["discordstaff"]["userids"].append(int(member.id))
                with open(staff_file, "w") as file:
                    json.dump(data, file, indent=4)
                await ctx.send(f"User {member.mention} Id: {member.id} Added To Owner")
        elif action == "remove":
            if int(member.id) not in data["discordstaff"]["userids"]:
                await ctx.send("User Is Not An Admin")
            else:
                data["discordstaff"]["userids"].pop(int(member.id))
                with open(staff_file, "w") as file:
                    json.dump(data, file, indent=4)
                await ctx.send(f"<@{member.id}> Has Been Removed From Admin List")
        else:
            await ctx.send("Use Action As add/remove")
    except Exception as e:
        await ctx.send(e)
        print(e)
        pass

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

async def server_logs():
    try:
        with open(logs_path, "r") as file:
            lines = file.readlines()
        if not lines:
            return "Empty"
        if len(lines) > 20:
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
    global msgchannel
    global guild_id
    try:
        data = await read_data_from_file()
        player = await players()
        guild = bot.get_guild(guild_id)
        channel = bot.get_channel(msgchannel)
        msgid = bot_msg[-1]
        message = await channel.fetch_message(msgid)
        embed = discord.Embed(title=f"`{server_name}`", description=f"**Live Players**```{player}```", color=0xA020F0)
        boticon = None
        if bot.user.avatar.url is not None:
            boticon = bot.user.avatar.url
        else:
            boticon = None
        embed.add_field(name="Live Chat", value=f"```{data}```")
        embed.set_footer(text=discord_server_name, icon_url=boticon)
        embed.set_author(name=discord_server_name, icon_url=guild.icon.url)
        await message.edit(content=None, embed=embed)
    except Exception as e:
        print(e)

async def server_log():
    try:
        data = await server_logs()
        guild = bot.get_guild(guild_id)
        channel = bot.get_channel(logschannel)
        msgid = log_msg[-1]
        message = await channel.fetch_message(msgid)
        boticon = None
        if bot.user.avatar.url is not None:
            boticon = bot.user.avatar.url
        else:
            boticon = None
        embed = discord.Embed(title=f"Server Logs", description=data, color=0xA020F0)
        embed.set_footer(text=discord_server_name, icon_url=boticon)
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

@tasks.loop(seconds=5)
async def serverlog():
    await server_log()

@serverlog.before_loop
async def before_update_message_task():
    await bot.wait_until_ready()

# Commands
@check()
@bot.command()
async def send(ctx, *, message: str):
    try:
        
        _ba.pushcall(Call(bs.chatmessage, message, sender_override=ctx.author.name), from_other_thread=True)
        msg = ctx.message
        await msg.add_reaction("✔️")
    except Exception as e:
        msg = ctx.message
        await msg.add_reaction("❌")
        print(e)

@check()
@bot.command()
async def mp(ctx, maxplayers: int):
    try:
        cmd = "/mp " + str(maxplayers)
        _ba.pushcall(Call(bs.chatmessage, cmd), from_other_thread=True)
        await ctx.send(f"Set Maxplayers Limit To {maxplayers}")
    except Exception as e:
        await ctx.send(str(e))
        print(e)
        pass



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        message = ctx.message
        await message.add_reaction("💢")


        await ctx.send(str(error))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(str(error))
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send(str(error))

    if isinstance(error, commands.BadArgument):
        await ctx.send(str(error))

    if isinstance(error, commands.CommandInvokeError):
        print(str(error))

        await ctx.send(str(error))



import requests

import bs4

import lxml

def _make_request_safe(request, retries=2,raise_err=True):
  try:
    return request
  except:
    if retries > 0:
       time.sleep(1)
       return _make_request_safe(request,retries=retries - 1, raise_err=raise_err)
    if raise_err:
       raise


    



  import requests
  import datetime

def get_acc_creation(pb_id):
    try:
        response = requests.get(f"https://legacy.ballistica.net/accountquery?id={pb_id}")
        dateacc = response.json()

        print("Response:", response.text)  # Add this line for debugging

        cre_time = dateacc["created"]
        dta = datetime.datetime(*map(int, cre_time))
        return dta
    except Exception as e:
        print("Error:", str(e))  # Add this line for debugging
        return "Unknown"

  # Test the function
  
  
@bot.command()

async def id(ctx, pb_id):


  result = requests.get(f"http://bombsquadgame.com/bsAccountInfo?buildNumber=20258&accountID={pb_id}")

  create = get_acc_creation(pb_id)
  data = result.json()
  print(data)
  l = data["accountDisplayStrings"]
  acs = str(l)
  ads = acs.replace("[", "").replace("]", "").replace("'", "")
  em = discord.Embed(title="Account Found", description=f"**Pb-id** = {pb_id}",color=0x00FFFF)
  em.add_field(name="Account Name",value=data["profileDisplayString"],inline=False)
  em.add_field(name="Accounts",value=ads,inline=False)
  em.add_field(name="Achievements Completed",value=data["achievementsCompleted"],inline=False)
  em.add_field(name="Created At",value=create,inline=False)
  em.set_thumbnail(url="https://cdn.discordapp.com/emojis/1001945225557721179.png?v=1&size=48&quality=lossless")
  
  await ctx.send(embed=em)
  
@check()
@bot.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, member: discord.Member, role: discord.Role):
    try:
        if role not in member.roles:
            await member.add_roles(role)
            embed = discord.Embed(title="Added Role",description=f"{role.mention} Given To {member.mention}",color=0x00FF00)
        else:
            await member.remove_roles(role)
            embed = discord.Embed(title="Removed Role", description=f"{role.mention} Removed From {member.mention}",color=0x00FF00)
    except Exception as e:
        embed = discord.Embed(title="Error", description=e,color=0xFF0000)
    await ctx.send(embed=embed)
        






def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')

@check()
@bot.command(hidden=True, name='eval')
async def eval(ctx: commands.Context, *, body: str):
    """Evaluates a code"""
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
    }
    env.update(globals())
    body = cleanup_code(body)
    stdout = io.StringIO()
    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass
        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            await ctx.send(f'```py\n{value}{ret}\n```')

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

