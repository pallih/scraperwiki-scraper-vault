# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_hani')


news_scraper.base_url            = 'http://www.mt.co.kr/common/list_second.htm?type=1&pDepth1=medi&pDepth2=Mhealth'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 15
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'cp949'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : 'id("artcle_all_list")/ul/li' },
    'title'   : {
        'xpath'   : './/dt[@class="title"]/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './/dd[@class="text"]/a',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/em[@class="date"]',
        'strip'   : False,
        'format'  : '%Y.%m.%d&nbsp;%H:%M'
    },
    'source'  : {
        'default' : '머니투데이'
    }
}


news_scraper.main()