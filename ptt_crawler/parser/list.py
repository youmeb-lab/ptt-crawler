# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

__all__ = ("parse")


def parse(html):
    soup = BeautifulSoup(html)
    url = parse_prev_page_url(soup)

    if url is None:
        return None

    return {
        "prev_page_url": url,
        "article_list": parse_article_list(soup),
    }


def parse_prev_page_url(soup):
    links = soup.select(".action-bar .pull-right .btn")
    url = None

    try:
        url = links[1].get("href")
    except:
        pass

    return url


def parse_article_list(soup):
    links = soup.select(".r-ent a")
    links = [link.get('href') for link in links]
    return links
