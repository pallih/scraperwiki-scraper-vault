# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://news.sportsseoul.com/list/health/101190100000000'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 10
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'utf-8'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//div[@class="lead_allnews02"]/ul' },
    'title'   : {
        'xpath'   : './/li/a[@class="b"]',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/li/a[@class="b"]/parent::li/following-sibling::li/a',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/li/a[@class="b"]/parent::li/following-sibling::li[1]',
        'strip'   : False,
        'format'  : '%Y-%m-%d %H:%M'
    },
    'source'  : {
        'default' : '스포츠서울'
    }
}


news_scraper.main()# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://news.sportsseoul.com/list/health/101190100000000'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 10
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'utf-8'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//div[@class="lead_allnews02"]/ul' },
    'title'   : {
        'xpath'   : './/li/a[@class="b"]',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/li/a[@class="b"]/parent::li/following-sibling::li/a',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/li/a[@class="b"]/parent::li/following-sibling::li[1]',
        'strip'   : False,
        'format'  : '%Y-%m-%d %H:%M'
    },
    'source'  : {
        'default' : '스포츠서울'
    }
}


news_scraper.main()