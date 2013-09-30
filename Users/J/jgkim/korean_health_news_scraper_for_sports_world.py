# coding=utf-8

import scraperwiki

news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://www.sportsworldi.com/Articles/LEISURELIFE/List.asp?subctg1=15&subctg2=00'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 15
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'euc-kr'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//div[@class="newsListFull-Text"]/div//ul' },
    'url'     : {
        'xpath'   : './a',
        'strip'   : False
    },
    'title'   : {
        'xpath'   : './/li[@class="T"]',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/li[@class="M"]',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/li[@class="B"]',
        'strip'   : False,
        'format'  : '[%Y/%m/%d]'
    },
    'source'  : {
        'default' : '스포츠월드'
    }
}


news_scraper.main()# coding=utf-8

import scraperwiki

news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://www.sportsworldi.com/Articles/LEISURELIFE/List.asp?subctg1=15&subctg2=00'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 15
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'euc-kr'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//div[@class="newsListFull-Text"]/div//ul' },
    'url'     : {
        'xpath'   : './a',
        'strip'   : False
    },
    'title'   : {
        'xpath'   : './/li[@class="T"]',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/li[@class="M"]',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/li[@class="B"]',
        'strip'   : False,
        'format'  : '[%Y/%m/%d]'
    },
    'source'  : {
        'default' : '스포츠월드'
    }
}


news_scraper.main()