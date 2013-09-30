# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_hani')


news_scraper.base_url            = 'http://life.joinsmsn.com/news/list/list.asp?sid=5119'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 15
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'utf-8'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : 'id("life_list")/div/ul/li' },
    'title'   : {
        'xpath'   : './/a[@class="title_cr"]',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/a[@class="read_cr"]',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/span[@class="date"]',
        'strip'   : False,
        'format'  : '%Y-%m-%d'
    },
    'source'  : {
        'default' : '중앙일보'
    }
}


news_scraper.main()# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_hani')


news_scraper.base_url            = 'http://life.joinsmsn.com/news/list/list.asp?sid=5119'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 15
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'utf-8'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : 'id("life_list")/div/ul/li' },
    'title'   : {
        'xpath'   : './/a[@class="title_cr"]',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/a[@class="read_cr"]',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/span[@class="date"]',
        'strip'   : False,
        'format'  : '%Y-%m-%d'
    },
    'source'  : {
        'default' : '중앙일보'
    }
}


news_scraper.main()