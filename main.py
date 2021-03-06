import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
import json

def load_config():
    with open("./data/config.json", mode="r", encoding="utf-8") as config_file:
        global config
        config = json.load(config_file)
def get_cogs():
    with open("./data/cogs.json", mode="r", encoding="utf-8") as cogs_file:
        global cogs
        cogs = json.load(cogs_file)["cogs"]

load_dotenv()
load_config()
get_cogs()
bot = discord.Bot(debug_guilds=[985045688377282581], intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("="*15)
    print(f"{bot.user} is ready and online!")
    print("="*15)
    return

@bot.slash_command(name = "reload", description = "Reload cog")
@commands.has_any_role(config["admin"])
async def reload(ctx:discord.ApplicationContext):
    try:
        load_config()
        get_cogs()
        for cog in cogs:
            try:
                bot.reload_extension(f"cogs.{cog}")
            except:
                bot.load_extension(f"cogs.{cog}")
    except:
        await ctx.respond("Error")
    else:
        await ctx.respond("Reload complete")
    return

for cog in cogs:
    bot.load_extension(f"cogs.{cog}")

keep_alive()
try:
    bot.run(os.getenv('TOKEN'))
except:
    os.system("kill 1")
