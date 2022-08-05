import string
import connection as conn


def search_article_by_id(key):
    r = conn.redis_init()
    if r is not None:
        if r.hexists(key, 'content'):
            return r.hmget(key, ['category', 'content', 'id', 'img'])  # category, content, id, img
    return ['N/A', 'N/A', 'N/A', 'None']


def search_article_by_category(search_index: int, limit=5):
    index_pair = {1: "靠北麥塊", 2: "告白麥塊", 3: "考古麥塊", 4: "迷因麥塊",
                  5: "靠北麥塊主機商", 6: "靠北麥塊代購商", 0: "所有分類"}

    r = conn.redis_init()
    db_size, max_id = r.dbsize(), r.dbsize() + 100
    article_dict = {}

    def get_requested_data():
        num_list, count = [], 0
        for i in range(max_id):
            if count < limit and r.hexists((max_id - i), 'category'):
                if search_index != 0:
                    if r.hget((max_id - i), 'category').decode('utf-8') == index_pair[search_index]:
                        num_list.append(max_id - i)
                        count = count + 1
                else:
                    num_list.append(max_id-i)
                    count = count + 1
        return num_list

    def get_article_content(key):
        return r.hget(key, 'content')

    for k in get_requested_data():
        prefix = "文章編號" + str(k)
        article_dict[prefix] = get_article_content(k).decode('utf-8')

    return index_pair[search_index], article_dict


def article_formatter(article: string, key):
    formatted_article = article.replace("\r", "")
    formatted_article = formatted_article.replace("靠北麥塊" + str(key), "")
    return formatted_article
