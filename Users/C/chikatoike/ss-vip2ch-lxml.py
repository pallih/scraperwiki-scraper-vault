#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)

import re
import lxml.html
import requests
import itertools


MAX_COUNT = 20

# プログラム上で使用するエンコーディング.
ENCODING = 'utf_8'

# スクラップ先のページのエンコーディング.
TARGET_ENCODING = 'utf_8'

TITLE_PATTERN = re.compile(u'.*(まどか|ほむら|さやか|マミ|杏子).*')

BASE_HREF = "http://ss.vip2ch.com"


def scrap(url):
    html = requests.get(url).content
    root = lxml.html.fromstring(html.decode(TARGET_ENCODING))
    items = root.xpath('//*[@id="mw-content-text"]/ul/li/a[not(contains(@class, "new"))]')

    t = items[0]
    print(lxml.html.tostring(t, method='text', encoding=ENCODING))
    # print(t.get('title').encode(ENCODING))

    items = (t for t in items if TITLE_PATTERN.match(t.get('title')))
    items = itertools.islice(items, MAX_COUNT)

    def prepare(item):
        item.make_links_absolute(BASE_HREF, resolve_base_href=True)
        return item

    items = itertools.imap(prepare, items)
    items = ({'url': t.get('href'), 'title': t.get('title')} for t in items)
    items = (fetch_detail(d['url'], d) for d in items)

    def process(item):
        print('-------------------')
        print(item['title'].encode(ENCODING))
        print(item['description'].encode(ENCODING))
        return item

    items = itertools.imap(process, items)

    try:
        import scraperwiki
        unique_keys = ['url']
        if hasattr(scraperwiki, 'sql'):
            scraperwiki.sql.save(unique_keys, list(items))
        else:
            scraperwiki.sqlite.save(unique_keys, list(items))
    except ImportError:
        pass


def fetch_detail(url, detail):
    html = requests.get(url).content
    root = lxml.html.fromstring(html.decode(TARGET_ENCODING))
    summary = root.xpath('//*[@id="mw-content-text"]/h2[1]/following-sibling::node()[not(preceding-sibling::h2[2])]')
    # summary = root.xpath('//*[@id="mw-content-text"]/p[1]')
    # detail['description'] = lxml.html.tostring(summary[0], method='text', encoding=ENCODING)
    # detail['description'] = ''.join(s if issubclass(type(s), str) else s.text_content() for s in summary)
    detail['description'] = ''.join(s.text_content() if hasattr(s, 'text_content') else s for s in summary)
    return detail


# 二次創作スレ一覧からスクレイピング
scrap("http://ss.vip2ch.com/ss/%E4%BA%8C%E6%AC%A1%E5%89%B5%E4%BD%9C%E3%82%B9%E3%83%AC%E4%B8%80%E8%A6%A7")
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)

import re
import lxml.html
import requests
import itertools


MAX_COUNT = 20

# プログラム上で使用するエンコーディング.
ENCODING = 'utf_8'

# スクラップ先のページのエンコーディング.
TARGET_ENCODING = 'utf_8'

TITLE_PATTERN = re.compile(u'.*(まどか|ほむら|さやか|マミ|杏子).*')

BASE_HREF = "http://ss.vip2ch.com"


def scrap(url):
    html = requests.get(url).content
    root = lxml.html.fromstring(html.decode(TARGET_ENCODING))
    items = root.xpath('//*[@id="mw-content-text"]/ul/li/a[not(contains(@class, "new"))]')

    t = items[0]
    print(lxml.html.tostring(t, method='text', encoding=ENCODING))
    # print(t.get('title').encode(ENCODING))

    items = (t for t in items if TITLE_PATTERN.match(t.get('title')))
    items = itertools.islice(items, MAX_COUNT)

    def prepare(item):
        item.make_links_absolute(BASE_HREF, resolve_base_href=True)
        return item

    items = itertools.imap(prepare, items)
    items = ({'url': t.get('href'), 'title': t.get('title')} for t in items)
    items = (fetch_detail(d['url'], d) for d in items)

    def process(item):
        print('-------------------')
        print(item['title'].encode(ENCODING))
        print(item['description'].encode(ENCODING))
        return item

    items = itertools.imap(process, items)

    try:
        import scraperwiki
        unique_keys = ['url']
        if hasattr(scraperwiki, 'sql'):
            scraperwiki.sql.save(unique_keys, list(items))
        else:
            scraperwiki.sqlite.save(unique_keys, list(items))
    except ImportError:
        pass


def fetch_detail(url, detail):
    html = requests.get(url).content
    root = lxml.html.fromstring(html.decode(TARGET_ENCODING))
    summary = root.xpath('//*[@id="mw-content-text"]/h2[1]/following-sibling::node()[not(preceding-sibling::h2[2])]')
    # summary = root.xpath('//*[@id="mw-content-text"]/p[1]')
    # detail['description'] = lxml.html.tostring(summary[0], method='text', encoding=ENCODING)
    # detail['description'] = ''.join(s if issubclass(type(s), str) else s.text_content() for s in summary)
    detail['description'] = ''.join(s.text_content() if hasattr(s, 'text_content') else s for s in summary)
    return detail


# 二次創作スレ一覧からスクレイピング
scrap("http://ss.vip2ch.com/ss/%E4%BA%8C%E6%AC%A1%E5%89%B5%E4%BD%9C%E3%82%B9%E3%83%AC%E4%B8%80%E8%A6%A7")
