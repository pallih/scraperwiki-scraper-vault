# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_hani')


news_scraper.base_url            = 'http://news.donga.com/It/Medi/2&'
news_scraper.page_param          = 's=%d'
news_scraper.page_num_of_article = 15
news_scraper.page_start          = 0
news_scraper.page_step           = news_scraper.page_num_of_article
news_scraper.page_encoding       = 'euc-kr'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//div[@class="rightList"]' },
    'title'   : {
        'xpath'   : './/p[@class="title"]/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/p[@class="text"]/a',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/p[@class="title"]/span',
        'strip'   : False,
        'format'  : '[%Y-%m-%d %H:%M:%S]'
    },
    'source'  : {
        'default' : '동아일보'
    }
}


news_scraper.main()# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_hani')


news_scraper.base_url            = 'http://news.donga.com/It/Medi/2&'
news_scraper.page_param          = 's=%d'
news_scraper.page_num_of_article = 15
news_scraper.page_start          = 0
news_scraper.page_step           = news_scraper.page_num_of_article
news_scraper.page_encoding       = 'euc-kr'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//div[@class="rightList"]' },
    'title'   : {
        'xpath'   : './/p[@class="title"]/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/p[@class="text"]/a',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/p[@class="title"]/span',
        'strip'   : False,
        'format'  : '[%Y-%m-%d %H:%M:%S]'
    },
    'source'  : {
        'default' : '동아일보'
    }
}


news_scraper.main()