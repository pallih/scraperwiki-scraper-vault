# coding=utf-8

import scraperwiki

news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://www.munhwa.com/news/section_list.html?sec=culture&class=10'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 15
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'euc-kr'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//html/body/div/table[4]/tr/td[1]/table[3]/tr/td[3]/table/tr/td/table/tr[2]' },
    'title'   : {
        'xpath'   : './/preceding-sibling::tr[1]/td/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/td/a',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/preceding-sibling::tr[1]/td/font',
        'strip'   : False,
        'format'  : '[%Y.%m.%d]'
    },
    'source'  : {
        'default' : '문화일보'
    }
}


news_scraper.main()# coding=utf-8

import scraperwiki

news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_yonhap_news')


news_scraper.base_url            = 'http://www.munhwa.com/news/section_list.html?sec=culture&class=10'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 15
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'euc-kr'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//html/body/div/table[4]/tr/td[1]/table[3]/tr/td[3]/table/tr/td/table/tr[2]' },
    'title'   : {
        'xpath'   : './/preceding-sibling::tr[1]/td/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/td/a',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/preceding-sibling::tr[1]/td/font',
        'strip'   : False,
        'format'  : '[%Y.%m.%d]'
    },
    'source'  : {
        'default' : '문화일보'
    }
}


news_scraper.main()