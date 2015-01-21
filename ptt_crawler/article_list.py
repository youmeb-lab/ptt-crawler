# -*- coding: utf-8 -*-

NO_MORE_DATA_MESSAGE = "No more data!"


class ArticleList:
    def __init__(self, board, content=False):
        self.content = content
        self.board = board
        self.reset()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next_article()

    def next(self):
        return self.next_article()

    def next_article(self):
        if self.buffer_is_empty():
            self.next_page()
            if self.at_last_page:
                raise StopIteration

        article_url = self.buffer[self.buffer_cursor]
        self.buffer_cursor += 1

        if self.content:
            return self.board.get_data(article_url)

        return article_url

    def next_page(self):
        if self.at_last_page:
            raise Exception(NO_MORE_DATA_MESSAGE)

        count = 0
        data = None
        page_url = self.page_url

        while count is 0:
            data = self.board.get_data(page_url)

            if data is None:
                self.at_last_page = True
                self.buffer = None
                self.buffer_cursor = 0
                self.buffer_lastindex = -1
                return

            count = len(data["article_list"])
            page_url = data["prev_page_url"]

        self.buffer_cursor = 0
        self.buffer = data["article_list"]
        self.buffer_lastindex = count - 1
        self.page_url = page_url

    def buffer_is_empty(self):
        return self.buffer_cursor > self.buffer_lastindex

    def reset(self):
        self.page_url = "/index.html"
        self.at_last_page = False
        self.buffer = None
        self.buffer_cursor = 0
        self.buffer_lastindex = -1
