import string
import connection as conn


def search_article_by_id(key):
    r = conn.redis_init()

    if r is not None:
        if r.hexists(key, 'content'):
            return r.hmget(key, ['content', 'img'])

    return ['N/A', 'None']


def article_formatter(article: string, key):
    formatted_article = article.replace("\r", "")
    formatted_article = formatted_article.replace("靠北麥塊"+str(key), "")
    return formatted_article

