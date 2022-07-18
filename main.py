# Author: Ivan Cheung, Anson Tsang

import services as s
import embed as e
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# General Vars
prefix = os.getenv("PREFIX")
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print('目前登入身份：', bot.user)
    print('登入身份 ID：', bot.user.id)
    onActivity = discord.Game("使用 " + prefix + " help 尋找靠北文章")

    await bot.change_presence(status=discord.Status.online, activity=onActivity)


@bot.command(name="get", aliases=['g'])
async def _get(ctx, key=0):
    if key != 0:
        response = s.search_article_by_id(key)

        if response[0] != 'N/A':
            search = e.embedded_frame(key, [s.article_formatter(response[0].decode('utf-8'), key),
                                            response[1].decode('utf-8')])
        else:
            search = e.embedded_frame(key, ['N/A', 'None'])
    else:
        search = e.embedded_frame(key, ['N/A', 'None'])

    await ctx.send(embed=search)


@bot.command(name="help", aliases=['?'])
async def _help(ctx):
    await ctx.send("使用 cb!get <文章> 獲取文章資訊吧 ~")


bot.run(token)
