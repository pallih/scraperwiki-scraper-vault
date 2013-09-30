# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://www.seoul.co.kr/news/newsList.php?section=health100'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 18
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'euc-kr'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//div[@id="Newslist"] | //div[@id="Newslist2"]' },
    'title'   : {
        'xpath'   : './/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/following-sibling::div[@id="Newslistcon"][1] | .//following-sibling::div[@id="Newslist2con"][1]',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : '.',
        'strip'   : True,
        'format'  : '%Y-%m-%d',
        'start'   : -10,
        'end'     : None
    },
    'source'  : {
        'default' : '서울신문'
    }
}


news_scraper.main()# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://www.seoul.co.kr/news/newsList.php?section=health100'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 18
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'euc-kr'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//div[@id="Newslist"] | //div[@id="Newslist2"]' },
    'title'   : {
        'xpath'   : './/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/following-sibling::div[@id="Newslistcon"][1] | .//following-sibling::div[@id="Newslist2con"][1]',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : '.',
        'strip'   : True,
        'format'  : '%Y-%m-%d',
        'start'   : -10,
        'end'     : None
    },
    'source'  : {
        'default' : '서울신문'
    }
}


news_scraper.main()