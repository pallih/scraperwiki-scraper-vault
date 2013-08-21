# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_hani')


news_scraper.base_url            = 'http://news.khan.co.kr/kh_news/khan_art_list.html?code=900303&list_code=khan'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 20
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'cp949'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//div[@class="article"] | //div[@class="photoArticle"]' },
    'title'   : {
        'xpath'   : './/dl/dt/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/dl/dd',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/dl/dd/span',
        'strip'   : False,
        'format'  : '%Y %m/%d %H:%M'
    },
    'source'  : {
        'default' : '경향신문'
    }
}


news_scraper.main()