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
        
        _ba.pushcall(Call(bs.chatmessage, message, sender_override=ctx.author.name), from_other_thread=True)
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
        _ba.pushcall(Call(bs.get_foreground_host_session().max_players, maxplayers), from_other_thread=True)
        _ba.pushcall(Call(bs.set_public_party_max_size, maxplayers), from_other_thread=True)
        bs.broadcastmessage(f"Set Maxplayer Limit To {maxplayers}", color=(1, 0, 1))
        await ctx.send(f"Set Maxplayer Size To {maxplayers}")
    except Exception as e:
        print(e)



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

@bot.command()
async def load(ctx, extension):
	await bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
	 await bot.unload_extension(f"cogs.{extension}")



@bot.command()
async def reload(ctx, extension):
	await bot.unload_extension(f"cogs.{extension}")
	await bot.load_extension(f"cogs.{extension}")

	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'): 
			bot.load_extension(f'cogs.{filename[:-3]}')

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
        
@bot.command()
async def file(ctx, text: str):
    img = Image.open("black.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("cat.ttf",50)
    draw.text((0,150), text, (0,0,0), font = font, fill=(255,0,0))
    img.save("look.png")
    await ctx.send(file= discord.File("look.png"))

@bot.command()
async def list(ctx):
    try:
        roster = await players()
        await ctx.send(roster)
    except Exception as e:
        await ctx.send(e)
        pass





def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')

@bot.command(hidden=True, name='eval')
@commands.has_permissions(administrator=True)
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

