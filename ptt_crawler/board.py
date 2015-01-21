# -*- coding: utf-8 -*-

import re
import time
import requests
from .parser import routes
from .article_list import ArticleList

BASE_URL = "https://www.ptt.cc"
URL_FORMAT = "/bbs/{board}{path}"
REQUEST_FAILED_MESSAGE = "HTTP request failed! status: {status}, url: {url}"
UNKNOWN_PAGE_MESSAGE = "Unknown page {url}"
IS_URL = re.compile("^https?:\/\/")
PATH_WITH_BOARD_NAME = re.compile("^\/bbs\/(?:.+)\/")


class Board:
    def __init__(self, name, verify=True):
        self.name = name
        self.verify = verify
        self.cookies = dict(over18="1")

    def articles(self):
        return ArticleList(self)

    def get_data(self, url):
        url = self.get_url(url)
        parse = routes(url)

        while True:
            r = requests.get(url, verify=self.verify, cookies=self.cookies)

            if parse is None:
                raise Exception(UNKNOWN_PAGE_MESSAGE.format(url=url))

            if r.status_code == 503:
                time.sleep(2)
                continue

            if r.status_code is not 200:
                msg = REQUEST_FAILED_MESSAGE.format(url=url, status=r.status_code)
                raise Exception(msg)

            break

        return parse(r.text)

    def get_url(self, path):
        if IS_URL.search(path):
            return path

        if not PATH_WITH_BOARD_NAME.search(path):
            path = URL_FORMAT.format(board=self.name, path=path)

        return BASE_URL + path
