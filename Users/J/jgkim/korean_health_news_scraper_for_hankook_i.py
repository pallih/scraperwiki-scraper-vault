from lxml.etree import fromstring as parse_xml
import scraperwiki
import urlparse
import urllib
import urllib2
import time
import re
import math
import htmlentitydefs


base_url            = 'http://news.hankooki.com'
ajax_url            = 'http://news.hankooki.com/ArticleList/getXml.php'
page_param          = 'num'
page_num_of_article = 20
page_start          = 1
page_step           = 1
page_encoding       = 'euc-kr'
page_sleep          = 0
params              = {
    'mediaCd'    : 'hk',
    'section'    : 'life',
    'subSection' : 'medical',
    'pageLine'   : page_num_of_article,
    'pageBlock'  : 10
}

patterns = {
    'article' : {'xpath' : "/newsList/listData/gisaInfo" },
    'url'     : {
        'xpath'   : './/gsUrl',
        'strip'   : False
    },
    'title'   : {
        'xpath'   : './/gsTitle',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/gsSummary',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/cDateTime',
        'strip'   : False,
        'format'  : '%Y-%m-%d %H:%M:%S'
    },
    'source'  : {
        'default' : '한국일보'
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

        url     = base_url + get_text(article, 'url')
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
        #print title, date
        #print summary
        scraperwiki.sqlite.save(unique_keys=['title', 'date'], data=data)
        num_of_article += 1

        count += 1
        if start_over is True and count == 1: scraperwiki.sqlite.save_var('latest_article', str([title, date]))

    return num_of_article


def main():
    global base_url, ajax_url, page_param, page_num_of_article, page_start, page_step, page_encoding, page_sleep, count

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
        ('Referer', base_url),
        ('X-Requested-With', 'XMLHttpRequest')
    ]
    urllib2.install_opener(opener)

    error_count    = 0
    num_of_article = page_num_of_article
    while num_of_article == page_num_of_article:
        params[page_param] = last_page

        try:
            xml = scraperwiki.scrape(ajax_url, params)
        except urllib2.URLError, e:
            print 'Cannot reach the server:',
            if hasattr(e, 'reason'): print e.reason
            elif hasattr(e, 'code'): print e.code
            error_count += 1
            if error_count < 3: continue
            else: break

        # try:
        #     xml = xml.decode(page_encoding)
        # except UnicodeDecodeError:
        #     encoded = ''
        #     for word in xml.split(' '):
        #         try:
        #             encoded += word.decode(page_encoding) + ' '
        #         except UnicodeDecodeError:
        #             pass
        #     xml = encoded.rstrip()

        num_of_article = scrape(parse_xml(xml), latest_article, start_over)

        page = last_page / page_step
        if (page_start == 0): page += 1

        scraperwiki.sqlite.save_var('last_page', last_page)
        print 'Page', page, ',', num_of_article, 'article(s)'

        last_page += page_step
        time.sleep(page_sleep)

    
    scraperwiki.sqlite.save_var('last_page', -1)
    print 'Total %d article(s) have been scraped.' % count


main()