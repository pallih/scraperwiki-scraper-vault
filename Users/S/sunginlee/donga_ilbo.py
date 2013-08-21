from lxml.html import fromstring as parse_html
import scraperwiki
import urlparse
import urllib
import time
import re


base_url            = 'http://news.donga.com/It/Medi/2&'
page_param          = 's=%d'
page_num_of_article = 15
page_start          = 0
page_step           = page_num_of_article
page_encoding       = 'euc-kr'

patterns = {
    'article' : {'xpath' : '//div[@class="rightList"]/p[@class="title"]' },
    'title'   : {
        'xpath'   : './/a',
        'strip'   : False
    },
#    'summary' : {
#        'xpath'   : './/font[2]',
#        'strip'   : False
#    },
    'date'    : {
        'xpath'   : './/span',
        'strip'   : False,
        'format'  : '[%Y-%m-%d %H:%M:%S]'
    },
    'source'  : {
        'default' : '동아일보'
    }
}


def get_text(article, kind):
    global patterns

    if 'xpath' in patterns[kind]:
        element = article.xpath(patterns[kind]['xpath'])[0]

        if patterns[kind]['strip']:
            text = element.text_content()
        else:
            text = element.text
    else:
        text = patterns[kind]['default']

    return text.strip()


def scrape(root, latest_article=''):
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
        url     = article.xpath(patterns['title']['xpath'] + '/@href')[0]
        title   = get_text(article, 'title')
        # summary = get_text(article, 'summary')
        date    = get_text(article, 'date')
        date    = time.strptime(date, patterns['date']['format'])
        date    = time.strftime(date_format, date)
        source  = get_text(article, 'source')

        if latest_article != '' and url == latest_article: break

        data = {
            'url'     : url,
            'title'   : title,
            # 'summary' : summary,
            'date'    : date,
            'source'  : source
        }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
        num_of_article += 1

        count += 1
        if count == 1: scraperwiki.sqlite.save_var('latest_article', url)

    return num_of_article


def build_url(page):
    global base_url, page_param

    parsed_url = list(urlparse.urlparse(base_url))
    if '%' in page_param:
        parsed_url[2]    += page_param % page
    else:
        query             = urlparse.parse_qs(parsed_url[4])
        query[page_param] = page
        parsed_url[4]     = urllib.urlencode(query)

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
    global page_num_of_article, page_start, page_step, page_encoding, count

    count = 0

    last_page      = scraperwiki.sqlite.get_var('last_page', page_start)
    latest_article = ''
    if last_page == -1:
        last_page    = page_start
        latest_article = scraperwiki.sqlite.get_var('latest_article', '')

    num_of_article = page_num_of_article
    while num_of_article == page_num_of_article:
        page_url       = build_url(last_page)
        html           = scraperwiki.scrape(page_url).decode(page_encoding)
        num_of_article = scrape(parse_html(html), latest_article)

        scraperwiki.sqlite.save_var('last_page', last_page)
        last_page += page_step

        if not page_exists(html, last_page): break

    scraperwiki.sqlite.save_var('last_page', -1)
    print '%d article(s) have been scraped.' % count


main()