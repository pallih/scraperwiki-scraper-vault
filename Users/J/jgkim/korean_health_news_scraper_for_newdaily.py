# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_hani')


news_scraper.base_url            = 'http://www.newdaily.co.kr/news/section_list_all.html?sec_no=91'
news_scraper.page_param          = 'page'
news_scraper.page_num_of_article = 15
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'utf-8'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//ul[@class="ndSectionListArea"]' },
    'title'   : {
        'xpath'   : './li[@class="ndThumbTit"]/a',
        'strip'   : False
    },
    'summary' : {
        'xpath'   : './li[@class="ndThumbPs"]/a',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './li[@class="ndThumbTit"]/span[@class="ndArtTime"]',
        'strip'   : False,
        'format'  : '%Y.%m.%d %H:%M:%S'
    },
    'source'  : {
        'default' : '뉴데일리'
    }
}


news_scraper.main()