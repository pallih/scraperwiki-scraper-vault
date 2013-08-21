# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_hani')


news_scraper.base_url            = 'http://sports.khan.co.kr/news/page/art_list.html?list_code=skhan&mcode=LIFE4&setcd=LIFE4'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 12
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
        'default' : '스포츠경향'
    }
}


news_scraper.main()