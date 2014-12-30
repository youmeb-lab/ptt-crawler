# -*- coding: utf-8 -*-
# flake8: noqa

import re
from .list import parse as parse_list
from .article import parse as parse_article

ARTICLE_RE = re.compile("\/bbs\/\w+\/\w+\.\d+.\w+\.\w+\.html$")
LIST_RE = re.compile("\/index\d*\.html$")


def routes(url):
    return article_page(url) \
        or list_page(url)


def article_page(url):
    if ARTICLE_RE.search(url):
        return parse_article


def list_page(url):
    if LIST_RE.search(url):
        return parse_list
