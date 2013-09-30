# coding=utf-8

# Use BeautifulSoup Parser for Yonhap News's Broken HTML Pages
from lxml.html.soupparser import fromstring as parse_html
import scraperwiki
import urllib2
import time

news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://news.naver.com/main/hotissue/sectionList.nhn?mid=hot&mode=LSD&gid=311583&cid=307085&sid1=103'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 50
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'cp949'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'headline_article' : { 'xpath' : '//div[@class="issue_headline"]//ul[@class="type05"]/li/dl[@class="sum"]' },
    'headline_title'   : {
        'xpath'   : './dt[last()]/a',
        'strip'   : True
    },
    'headline_summary' : {
        'xpath'   : './dd',
        'strip'   : False
    },
    'sub_item'         : { 'xpath' : './following-sibling::ul[@class="sub_item"]/li' },
    'article'          : {'xpath' : '//div[@class="list_body"]/ul/li' },
    'title'            : {
        'xpath'   : './a',
        'strip'   : True
    },
    'summary'          : {
        'default' : ''
    },
    'date'             : {
        'xpath'   : './/span[@class="date"]',
        'strip'   : False,
        'format'  : '%Y-%m-%d'
    },
    'source'           : {
        'xpath'   : './/span[@class="writing"]',
        'strip'   : False
    }
}


def scrape(root):
    global news_scraper

    num_of_article = 0
    for headline in root.xpath(news_scraper.patterns['headline_article']['xpath']):
        headline.make_links_absolute(news_scraper.base_url)

        url     = headline.xpath(news_scraper.patterns['headline_title']['xpath'] + '/@href')[0]
        title   = news_scraper.get_text(headline, 'headline_title')
        summary = news_scraper.get_text(headline, 'headline_summary')
        date    = news_scraper.get_text(headline, 'date')
        source  = news_scraper.get_text(headline, 'source')

        if title == '':
            break
        elif date == '':
            num_of_article += 1
            print 'Skip 1 article that has no date'
            continue

        date = time.strptime(date, news_scraper.unescape(news_scraper.patterns['date']['format']))
        date = time.strftime('%Y-%m-%d', date)

        key  = str([title, date])
        data = {
            'url'     : url,
            'title'   : title,
            'summary' : summary,
            'date'    : date,
            'source'  : source
        }
        scraperwiki.sqlite.save(unique_keys=['title', 'date'], data=data)
        num_of_article += 1

        for article in headline.xpath(news_scraper.patterns['sub_item']['xpath']):
            article.make_links_absolute(news_scraper.base_url)

            url     = article.xpath(news_scraper.patterns['title']['xpath'] + '/@href')[0]
            title   = news_scraper.get_text(article, 'title')
            summary = news_scraper.get_text(article, 'summary')
            date    = news_scraper.get_text(article, 'date')
            source  = news_scraper.get_text(article, 'source')
    
            if title == '':
                break
            elif date == '':
                num_of_article += 1
                print 'Skip 1 article that has no date'
                continue
    
            date = time.strptime(date, news_scraper.unescape(news_scraper.patterns['date']['format']))
            date = time.strftime('%Y-%m-%d', date)
    
            data = {
                'url'     : url,
                'title'   : title,
                'summary' : summary,
                'date'    : date,
                'source'  : source
            }
            scraperwiki.sqlite.save(unique_keys=['title', 'date'], data=data)
            num_of_article += 1

    return num_of_article


def main():
    global news_scraper

    opener = urllib2.build_opener()
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0'),
        ('Referer', news_scraper.base_url)
    ]
    urllib2.install_opener(opener)

    error_count = 0
    while error_count < 3:
        try:
            html = scraperwiki.scrape(news_scraper.base_url)
        except urllib2.URLError, e:
            print 'Cannot reach the server:',
            if hasattr(e, 'reason'): print e.reason
            elif hasattr(e, 'code'): print e.code
            error_count += 1

        try:
            html = html.decode(news_scraper.page_encoding)
        except UnicodeDecodeError:
            encoded = ''
            for word in html.split(' '):
                try:
                    encoded += word.decode(news_scraper.page_encoding) + ' '
                except UnicodeDecodeError:
                    pass
            html = encoded.rstrip()

        num_of_article = scrape(parse_html(html))

        print 'Headline ,', num_of_article, 'article(s)'
        break

    news_scraper.main()


main()# coding=utf-8

# Use BeautifulSoup Parser for Yonhap News's Broken HTML Pages
from lxml.html.soupparser import fromstring as parse_html
import scraperwiki
import urllib2
import time

news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://news.naver.com/main/hotissue/sectionList.nhn?mid=hot&mode=LSD&gid=311583&cid=307085&sid1=103'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 50
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'cp949'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'headline_article' : { 'xpath' : '//div[@class="issue_headline"]//ul[@class="type05"]/li/dl[@class="sum"]' },
    'headline_title'   : {
        'xpath'   : './dt[last()]/a',
        'strip'   : True
    },
    'headline_summary' : {
        'xpath'   : './dd',
        'strip'   : False
    },
    'sub_item'         : { 'xpath' : './following-sibling::ul[@class="sub_item"]/li' },
    'article'          : {'xpath' : '//div[@class="list_body"]/ul/li' },
    'title'            : {
        'xpath'   : './a',
        'strip'   : True
    },
    'summary'          : {
        'default' : ''
    },
    'date'             : {
        'xpath'   : './/span[@class="date"]',
        'strip'   : False,
        'format'  : '%Y-%m-%d'
    },
    'source'           : {
        'xpath'   : './/span[@class="writing"]',
        'strip'   : False
    }
}


def scrape(root):
    global news_scraper

    num_of_article = 0
    for headline in root.xpath(news_scraper.patterns['headline_article']['xpath']):
        headline.make_links_absolute(news_scraper.base_url)

        url     = headline.xpath(news_scraper.patterns['headline_title']['xpath'] + '/@href')[0]
        title   = news_scraper.get_text(headline, 'headline_title')
        summary = news_scraper.get_text(headline, 'headline_summary')
        date    = news_scraper.get_text(headline, 'date')
        source  = news_scraper.get_text(headline, 'source')

        if title == '':
            break
        elif date == '':
            num_of_article += 1
            print 'Skip 1 article that has no date'
            continue

        date = time.strptime(date, news_scraper.unescape(news_scraper.patterns['date']['format']))
        date = time.strftime('%Y-%m-%d', date)

        key  = str([title, date])
        data = {
            'url'     : url,
            'title'   : title,
            'summary' : summary,
            'date'    : date,
            'source'  : source
        }
        scraperwiki.sqlite.save(unique_keys=['title', 'date'], data=data)
        num_of_article += 1

        for article in headline.xpath(news_scraper.patterns['sub_item']['xpath']):
            article.make_links_absolute(news_scraper.base_url)

            url     = article.xpath(news_scraper.patterns['title']['xpath'] + '/@href')[0]
            title   = news_scraper.get_text(article, 'title')
            summary = news_scraper.get_text(article, 'summary')
            date    = news_scraper.get_text(article, 'date')
            source  = news_scraper.get_text(article, 'source')
    
            if title == '':
                break
            elif date == '':
                num_of_article += 1
                print 'Skip 1 article that has no date'
                continue
    
            date = time.strptime(date, news_scraper.unescape(news_scraper.patterns['date']['format']))
            date = time.strftime('%Y-%m-%d', date)
    
            data = {
                'url'     : url,
                'title'   : title,
                'summary' : summary,
                'date'    : date,
                'source'  : source
            }
            scraperwiki.sqlite.save(unique_keys=['title', 'date'], data=data)
            num_of_article += 1

    return num_of_article


def main():
    global news_scraper

    opener = urllib2.build_opener()
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0'),
        ('Referer', news_scraper.base_url)
    ]
    urllib2.install_opener(opener)

    error_count = 0
    while error_count < 3:
        try:
            html = scraperwiki.scrape(news_scraper.base_url)
        except urllib2.URLError, e:
            print 'Cannot reach the server:',
            if hasattr(e, 'reason'): print e.reason
            elif hasattr(e, 'code'): print e.code
            error_count += 1

        try:
            html = html.decode(news_scraper.page_encoding)
        except UnicodeDecodeError:
            encoded = ''
            for word in html.split(' '):
                try:
                    encoded += word.decode(news_scraper.page_encoding) + ' '
                except UnicodeDecodeError:
                    pass
            html = encoded.rstrip()

        num_of_article = scrape(parse_html(html))

        print 'Headline ,', num_of_article, 'article(s)'
        break

    news_scraper.main()


main()