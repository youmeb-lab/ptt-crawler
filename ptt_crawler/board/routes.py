import re
import pttparser as parser

ARTICLE_RE = re.compile("\/bbs\/\w+\/\w+\.\d+.\w+\.\w+\.html$")
LIST_RE = re.compile("\/index\d*\.html$")


def routes(url):
    return articlePage(url) \
        or listPage(url)


def articlePage(url):
    if ARTICLE_RE.search(url):
        return parser.parse_article


def listPage(url):
    if LIST_RE.search(url):
        return parser.parse_list
