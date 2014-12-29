import requests
from .routes import routes

URL_FORMAT = "https://www.ptt.cc/${board}/index.html"
REQUEST_FAILED_MESSAGE = "HTTP request failed! ${url}"
NO_MORE_DATA_MESSAGE = "No more data!"


class PttBoard:
    def __init__(self, name):
        self.name = name
        self.cookie = {}
        self.page_url = "".format(board=name)
        self.at_last_page = False
        self.buffer = None
        self.buffer_cursor = 0
        self.buffer_lastindex = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next_article()

    def next_article(self):
        if self.buffer_is_empty():
            if self.at_last_page:
                raise StopIteration
            else:
                self.next_page()

        article = self.buffer[self.buffer_cursor]
        self.buffer_cursor += 1

        return article

    def next_page(self):
        if self.at_last_page:
            raise Exception(NO_MORE_DATA_MESSAGE)

        data = self.get_data(self.page_url)

        if data is None:
            self.at_last_page = True
            self.buffer = None
            self.buffer_cursor = 0
            self.buffer_lastindex = -1
            return

        self.buffer_cursor = 0
        self.buffer = data.list
        self.buffer_lastindex = len(data.list) - 1
        self.page_url = data.prev_page_url

    def buffer_is_empty(self):
        return self.buffer_cursor >= self.self.buffer_lastindex

    def get_data(self, url):
        parse = routes(url)
        r = requests.get(url, cookies=self.cookies)

        if r.status_code is not 200:
            raise Exception(REQUEST_FAILED_MESSAGE.format(url=url))

        return parse(r.text)
