import discord


def embedded_frame(key, article_content_list: list):
    embed = discord.Embed(title="靠北麥塊搜尋器 CBMC Searcher", description="每天晚上凌晨12點重新獲取上一天的最新資訊")
    embed.add_field(name="文章編號", value="靠北麥塊 " + str(key), inline=False)

    if article_content_list[0] != "N/A":
        embed.add_field(name="文章內容", value=article_content_list[0], inline=False)
    else:
        embed.add_field(name="文章內容", value="沒有文章 " + str(key) + " 的資料，請確認後再查詢。", inline=False)

    if article_content_list[1] != "None":
        embed.set_image(url=article_content_list[1])

    embed.set_footer(text="靠北麥塊搜尋器 | Ivan Cheung (HyperNitePo.)")
    return embed

