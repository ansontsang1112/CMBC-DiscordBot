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
    onActivity = discord.Game("使用 " + prefix + "help 尋找靠北文章")

    await bot.change_presence(status=discord.Status.online, activity=onActivity)


@bot.command(name="get", aliases=['g'])
async def _get(ctx, key=0):
    if key != 0:
        response = s.search_article_by_id(key)
        if response[1] != 'N/A':
            search = e.embedded_frame(key, [response[0].decode('utf-8'),
                                            s.article_formatter(response[1].decode('utf-8'), key),
                                            response[3].decode('utf-8')])
        else:
            search = e.embedded_frame(key, ['N/A', 'N/A', 'None'])
    else:
        search = e.embedded_frame(key, ['N/A', 'N/A', 'None'])

    await ctx.send(embed=search)


@bot.command(name="list", aliases=['l'])
async def _list(ctx, category=-1, limit=5):
    if limit <= 50:
        if category != -1:
            await ctx.send("搜索引擎：正在努力載入相關數據 ...")
            category_name, response = s.search_article_by_category(category, limit)
            embed = e.general_embedded_frame("關於最新 " + str(limit) + " 的「" + category_name + "」貼文。", response)
            await ctx.send(embed=embed)
        else:
            inline = {"靠北麥塊": "搜索編號：1", "告白麥塊": "搜索編號：2", "考古麥塊": "搜索編號：3", "迷因麥塊": "搜索編號：4",
                      "靠北麥塊主機商": "搜索編號：5", "靠北麥塊代購商": "搜索編號：6", "列出昨天最新 5 個貼文 ": "搜索編號：0"}
            embed = e.general_embedded_frame("根據分類列出最新十個的「靠北麥塊」貼文！編號對照表：", inline,
                                             "使用 " + prefix + "list <類別> {數量} 列出文章")
            await ctx.send(embed=embed)
    else:
        await ctx.send("搜索引擎：由於文字顯示限制，最多可支持搜尋 50 篇文章！")


@bot.command(name="help", aliases=['?'])
async def _help(ctx):
    await ctx.send(embed=e.help_embedded_frame(prefix))


bot.run(token)
