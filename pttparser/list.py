from bs4 import BeautifulSoup

__all__ = ("parse")


def parse(html):
    soup = BeautifulSoup(html)
    links = soup.select(".r-ent a")
    links = [link.get('href') for link in links]
    return links
