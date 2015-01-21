# -*- coding: utf-8 -*-

"""
    處理文章頁面資料
"""

import re
from functools import reduce
from bs4 import BeautifulSoup

__all__ = ("parse")

IS_REPLY = re.compile("^\s*RE:")
PARSE_TITLE = re.compile("(?:\[(.*?)\])?\s*(.*)$")

META_NAMES = {
    u"作者": "author",
    u"看板": "board",
    u"標題": "title",
    u"時間": "time",
}


def parse(html):
    data = {}
    soup = BeautifulSoup(html)
    main = soup.find(id="main-content")

    for node in main.contents:
        parse_node(node, data)

    data["content"] = data.get("content", "").strip()

    return data


def parse_node(node, context):
    parse_meta(node, context)\
        or parse_comment(node, context)\
        or parse_content(node, context)


def parse_meta(node, context):
    if is_element(node) and is_meta(node):
        meta = context.get("meta", {})

        key = node.select(".article-meta-tag")
        val = node.select(".article-meta-value")

        if len(val) is 0 or len(key) is 0:
            return True

        key = META_NAMES.get(key[0].text.strip(), "unknown")
        val = val[0].text.strip()
        meta[key] = val

        if key is "title":
            match = PARSE_TITLE.match(meta["title"])
            article_type = match.group(1)
            title = match.group(2)
            meta["type"] = article_type
            meta["title"] = title
            meta["re"] = True if IS_REPLY.search(title) else False

        context["meta"] = meta

        return True


def parse_comment(node, context):
    if is_element(node) and is_comment(node):
        tag = node.select(".push-tag")
        user = node.select(".push-userid")
        content = node.select(".push-content")
        time = node.select(".push-ipdatetime")

        if len(tag) and len(user) and len(time):
            comments = context.get("comments", [])
            comments.append({
                "tag": tag[0].text.strip(),
                "user": user[0].text.strip(),
                "time": time[0].text.strip(),
                "content": get_comment_content(content[0]),
            })
            context["comments"] = comments

        return True


def parse_content(node, context):
    context["content"] = context.get("content", "") + get_text(node)


def get_comment_content(comment_root):
    content = ""

    for node in comment_root.contents:
        content += get_text(node)

    return content.strip()


def get_text(node):
    if is_link(node):
        return node.get("href", "")
    elif is_image(node):
        return node.get("src", "")
    return node.text if is_element(node) else node


def is_element(node):
    return node.name


def is_link(node):
    return node.name is "a"


def is_image(node):
    return node.name is "img"


def is_comment(node):
    return has_class(node, "push")


def is_meta(node):
    return has_class(node, "article-metaline", "article-metaline-right")


def has_class(node, *args):
    expect = list(args)
    expect.insert(0, False)
    names = node.get("class", [])
    return reduce(lambda success, name: success or name in names, expect)
