# coding=utf-8

from lxml.html import fromstring as parse_html
import scraperwiki
import urlparse
import urllib
import urllib2
import time
import re
import math
import htmlentitydefs


base_url            = 'http://www.hani.co.kr/arti/society/health/'
page_param          = 'cline'
page_num_of_article = 10
page_start          = 0
page_step           = page_num_of_article
page_encoding       = 'euc-kr'
page_sleep          = 0

patterns = {
    'article' : {'xpath' : '//html/body/div/table/tr/td[2]/table/tr/td/table/tr[2]/td/table/tr/td[2]' },
    'title'   : {
        'xpath'   : './/font[1]/b/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/font[2]',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/font[2]/font',
        'strip'   : False,
        'format'  : '[%Y-%m-%d %H:%M]'
    },
    'source'  : {
        'default' : '한겨레'
    }
}


def unescape(text):
    def fix_up(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is

    return re.sub("&#?\w+;", fix_up, text)


def get_text(article, kind):
    global patterns

    text = ''
    if 'xpath' in patterns[kind]:
        try:
            element = article.xpath(patterns[kind]['xpath'])[0]
    
            if patterns[kind]['strip']:
                text = element.text_content()
            else:
                text = element.text
    
            if text is None:
                text = ''
            elif 'start' in patterns[kind]:
                text = text[patterns[kind]['start']:patterns[kind]['end']]
        except IndexError:
            pass
    elif 'default' in patterns[kind]:
        text = patterns[kind]['default']

    return unescape(text.strip())


def scrape(root, latest_article=None, start_over=False):
    global count, base_url, patterns

    num_of_article = 0
    for article in root.xpath(patterns['article']['xpath']):
        if re.search('(?i)(%Y)', patterns['date']['format']) is not None:
            date_format = '%Y-'
        else:
            date_format = time.strftime('%Y-')

        date_format += '%m-%d'

        if re.search('(%H)|(%I)', patterns['date']['format']) is not None:
            date_format += ' %H:%M'

        article.make_links_absolute(base_url)

        if 'url' in patterns:
            url = article.xpath(patterns['url']['xpath'] + '/@href')[0]
        else:
            url = article.xpath(patterns['title']['xpath'] + '/@href')[0]
        title   = get_text(article, 'title')
        summary = get_text(article, 'summary')
        date    = get_text(article, 'date')
        source  = get_text(article, 'source')

        if title == '':
            break
        elif date == '':
            num_of_article += 1
            print 'Skip 1 article that has no date'
            continue

        date = time.strptime(date, unescape(patterns['date']['format']))
        date = time.strftime(date_format, date)

        if latest_article is not None and latest_article == str([title, date]): break

        data = {
            'url'     : url,
            'title'   : title,
            'summary' : summary,
            'date'    : date,
            'source'  : source
        }
        scraperwiki.sqlite.save(unique_keys=['title', 'date'], data=data)
        num_of_article += 1

        count += 1
        if start_over is True and count == 1: scraperwiki.sqlite.save_var('latest_article', str([title, date]))

    return num_of_article


def build_url(page):
    global base_url, page_param

    parsed_url = list(urlparse.urlparse(base_url))
    if '%' in page_param:
        parsed_url[2]    += page_param % page
    else:
        query = urlparse.parse_qsl(parsed_url[4])
        query.append((page_param, page))
        parsed_url[4] = urllib.urlencode(query)

    return urlparse.urlunparse(parsed_url)


def page_exists(html, page):
    global page_param

    if '%' in page_param:
        query = page_param % page
    else:
        query = { page_param : page }
        query = urllib.urlencode(query)

    return query in html


def main():
    global base_url, page_num_of_article, page_start, page_step, page_encoding, page_sleep, count

    count = 0

    last_page      = scraperwiki.sqlite.get_var('last_page', -1)
    latest_article = None
    start_over     = False
    if last_page == -1:
        last_page      = page_start
        latest_article = scraperwiki.sqlite.get_var('latest_article', None)
        start_over     = True

    opener = urllib2.build_opener()
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0'),
        ('Referer', base_url)
    ]
    urllib2.install_opener(opener)

    error_count    = 0
    num_of_article = page_num_of_article
    while num_of_article == page_num_of_article:
        page_url = build_url(last_page)

        try:
            html = scraperwiki.scrape(page_url)
        except urllib2.URLError, e:
            print 'Cannot reach the server:',
            if hasattr(e, 'reason'): print e.reason
            elif hasattr(e, 'code'): print e.code
            error_count += 1
            if error_count < 3: continue
            else: break

        try:
            html = html.decode(page_encoding)
        except UnicodeDecodeError:
            encoded = ''
            for word in html.split(' '):
                try:
                    encoded += word.decode(page_encoding) + ' '
                except UnicodeDecodeError:
                    pass
            html = encoded.rstrip()

        num_of_article = scrape(parse_html(html), latest_article, start_over)

        page = last_page / page_step
        if (page_start == 0): page += 1

        scraperwiki.sqlite.save_var('last_page', last_page)
        print 'Page', page, ',', num_of_article, 'article(s)'

        last_page += page_step
        if not page_exists(html, last_page): break
        time.sleep(page_sleep)


    scraperwiki.sqlite.save_var('last_page', -1)
    print 'Total %d article(s) have been scraped.' % count


if __name__ == 'scraper': main()