# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://news.chosun.com/svc/list_in/list.html?catid=51&source=1'
news_scraper.page_param          = 'pn'
news_scraper.page_num_of_article = 10
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'euc-kr'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : "//dl[@class='article']" },
    'title'   : {
        'xpath'   : './/dt/span[1]/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/dd[@class="sub"]/span/a',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/dt/span[2]',
        'strip'   : False,
        'format'  : '%Y.%m.%d',
        'start'   : 0,
        'end'     : 10
    },
    'source'  : {
        'default' : '조선일보'
    }
}


news_scraper.main()# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://news.chosun.com/svc/list_in/list.html?catid=51&source=1'
news_scraper.page_param          = 'pn'
news_scraper.page_num_of_article = 10
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'euc-kr'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : "//dl[@class='article']" },
    'title'   : {
        'xpath'   : './/dt/span[1]/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/dd[@class="sub"]/span/a',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/dt/span[2]',
        'strip'   : False,
        'format'  : '%Y.%m.%d',
        'start'   : 0,
        'end'     : 10
    },
    'source'  : {
        'default' : '조선일보'
    }
}


news_scraper.main()