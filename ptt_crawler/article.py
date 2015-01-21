# -*- coding: utf-8 -*-

import re
from dateutil.parser import parse as parseTime

PARSE_ID = re.compile("((?:\w+\.){3}\w+)")


class Article:
    def __init__(self, path, board):
        self.path = path
        self.board = board
        self.data = {}

    def readable(self):
        return self.data.get("meta")

    @property
    def id(self):
        match = PARSE_ID.search(self.path)
        return match and match.group(1)

    @property
    def url(self):
        return self.board.get_url(self.path)

    @property
    def title(self):
        return self.get_meta_data("title")

    @property
    def author(self):
        return self.get_meta_data("author")

    @property
    def time(self):
        time = self.get_meta_data("time")
        return parseTime(time)

    @property
    def type(self):
        return self.get_meta_data("type")

    @property
    def reply(self):
        return self.get_meta_data("re")

    @property
    def content(self):
        return self.data.get("content")

    def get_meta_data(self, key, defval=None):
        meta = self.data.get("meta", {})
        return meta.get(key, defval)

    def fetch(self):
        self.data = self.board.get_data(self.path)
