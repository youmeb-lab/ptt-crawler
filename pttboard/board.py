import requests
from .routes import routes

BASE_URL = "https://www.ptt.cc"
URL_FORMAT = "/bbs/{board}/index.html"
REQUEST_FAILED_MESSAGE = "HTTP request failed! {url}"
NO_MORE_DATA_MESSAGE = "No more data!"
UNKNOWN_PAGE_MESSAGE = "Unknown page {url}"


class PTTBoard:
    def __init__(self, name):
        self.name = name
        self.cookies = dict(over18="1")
        self.page_url = URL_FORMAT.format(board=name)
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
            self.next_page()
            if self.at_last_page:
                raise StopIteration

        article_url = self.buffer[self.buffer_cursor]
        self.buffer_cursor += 1

        return self.get_data(article_url)

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
        self.buffer = data["article_list"]
        self.buffer_lastindex = len(data["article_list"]) - 1
        self.page_url = data["prev_page_url"]

    def buffer_is_empty(self):
        return self.buffer_cursor >= self.buffer_lastindex

    def get_data(self, url):
        parse = routes(url)
        r = requests.get(BASE_URL + url, cookies=self.cookies)

        if parse is None:
            raise Exception(UNKNOWN_PAGE_MESSAGE.format(url=url))

        if r.status_code is not 200:
            raise Exception(REQUEST_FAILED_MESSAGE.format(url=url))

        return parse(r.text)
