import interactions


def markdown(content):
    for ch in ['*','_','~','`']:
        content = content.replace(ch, '\\'+ch)
    return content


def embedded_frame(key, article_content_list: list):
    embed = interactions.Embed(title="靠北麥塊搜尋器 CBMC Searcher", description="每一小時重新獲取最新資訊")
    embed.add_field(name="文章編號", value="靠北麥塊 " + str(key), inline=False)

    if article_content_list[1] != "N/A":
        embed.add_field(name="文章內容", value=markdown(article_content_list[1]), inline=False)
        embed.add_field(name="文章分類", value=markdown(article_content_list[0]), inline=False)
    else:
        embed.add_field(name="文章內容", value="沒有文章 " + str(key) + " 的資料，請確認後再查詢。", inline=False)

    if article_content_list[2] != "None":
        embed.set_image(url=article_content_list[2])

    embed.set_footer(text="靠北麥塊搜尋器 | HyperNitePo.")
    return embed


def general_embedded_frame(description, inline_structure: dict, footer=""):
    embed = interactions.Embed(title="靠北麥塊搜尋器 CBMC Searcher", description=description)

    for key in inline_structure:
        embed.add_field(name=key, value=inline_structure[key], inline=False)

    embed.set_footer(text="靠北麥塊搜尋器 | HyperNitePo. | " + footer)
    return embed


def help_embedded_frame(prefix: str):
    embed = interactions.Embed(title="靠北麥塊搜尋器 CBMC Searcher", description="每一小時重新獲取最新資訊")

    embed.add_field(name="/get <文章編號>", value="根據 ID 獲取文章資訊", inline=False)
    embed.add_field(name="/list <類別> {列出數量 (如適用)}", value="根據「類別」搜尋文章", inline=False)

    embed.set_footer(text="靠北麥塊搜尋器 | HyperNitePo.")
    return embed

