# Author: Ivan Cheung, Anson Tsang
from ctypes import Union

from interactions import StatusType, PresenceActivityType, ClientPresence

import services as s
import embed as e
import os
import interactions

from dotenv import load_dotenv

load_dotenv()

# General Vars
prefix = os.getenv("PREFIX")
token = os.getenv("DEV_TOKEN")
bot = interactions.Client(command_prefix=prefix, token=token)


@bot.event
async def on_ready():
    print('「靠北麥塊搜尋器」啟動成功！')
    activity = interactions.PresenceActivity(name="使用 /help 尋找靠北文章", type=PresenceActivityType.LISTENING)
    await bot.change_presence(
        ClientPresence(
            status=StatusType.ONLINE,
            activities=[activity]
        )
    )


@bot.command(
    name="get",
    description="搜尋「靠北麥塊」文章",
    options=[
        interactions.Option(
            name="key",
            description="請輸入「文章ID」| ID 必定為數字",
            type=interactions.OptionType.INTEGER,
            required=True,
            autocomplete=True
        )
    ]
)
async def _get(ctx: interactions.CommandContext, key):
    if key is None:
        key = 0
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

    await ctx.send(embeds=search)


@bot.command(
    name="list",
    description="列出「靠北麥塊」文章（最多 30 篇章）| 不清楚分類可以先回車 (Enter) 觀看列表",
    options=[
        interactions.Option(
            name="category",
            description="請輸入「文章分類」| 不清楚分類可以先回車 (Enter) 觀看列表",
            type=interactions.OptionType.INTEGER,
            required=False,
            autocomplete=True,
        ),
        interactions.Option(
            name="limit",
            description="請輸入「導出數目」（暫時最多支援導出 30 篇文章）",
            type=interactions.OptionType.INTEGER,
            required=False,
            autocomplete=True
        )
    ]
)
async def _list(ctx: interactions.CommandContext, category=-1, limit=5):
    if limit <= 15:
        if 6 > category > -1:
            await ctx.send("搜索引擎：正在努力載入相關數據 ...")
            category_name, response = s.search_article_by_category(category, limit)
            embed = e.general_embedded_frame("關於最新 " + str(limit) + " 的「" + category_name + "」貼文。", response)
            await ctx.send(embeds=embed)
        else:
            inline = {"靠北麥塊": "搜索編號：1", "告白麥塊": "搜索編號：2", "考古麥塊": "搜索編號：3", "迷因麥塊": "搜索編號：4",
                      "靠北麥塊主機商": "搜索編號：5", "靠北麥塊代購商": "搜索編號：6", "列出昨天最新 5 個貼文 ": "搜索編號：0"}
            embed = e.general_embedded_frame("根據分類列出最新十個的「靠北麥塊」貼文！編號對照表：", inline,
                                             "使用 " + prefix + "list <類別> {數量} 列出文章")
            await ctx.send(embeds=embed)
    else:
        await ctx.send("搜索引擎：由於文字顯示限制，最多可支持搜尋 15 篇文章！")


@bot.command(name="help", description="「靠北麥塊搜尋器」幫助頁面")
async def _help(ctx: interactions.CommandContext):
    await ctx.send(embeds=e.help_embedded_frame(prefix))


bot.start()
