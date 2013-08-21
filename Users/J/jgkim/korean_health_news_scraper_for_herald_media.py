# coding=utf-8

import scraperwiki


news_scraper = scraperwiki.utils.swimport('korean_health_news_scraper_for_hani')


news_scraper.base_url            = 'http://biz.heraldm.com/common/List.jsp?ListId=010505000000'
news_scraper.page_param          = 'PageNo'
news_scraper.page_num_of_article = 15
news_scraper.page_start          = 1
news_scraper.page_step           = 1
news_scraper.page_encoding       = 'utf-8'
news_scraper.page_sleep          = 0

news_scraper.patterns = {
    'article' : {'xpath' : '//div[@class="contents_middle"]/ul[@class="newslist"]/li[@class="line"]/dl' },
    'title'   : {
        'xpath'   : './/dt/a',
        'strip'   : True
    },
    'summary' : {
        'xpath'   : './/dd[@class="txt"]/p/a',
        'strip'   : False
    },
    'date'    : {
        'xpath'   : './/dd[@class="date_write"]',
        'strip'   : False,
        'format'  : '%Y-%m-%d&nbsp;%H:%M',
        'start'   : -16,
        'end'     : None
    },
    'source'  : {
        'default' : '헤럴드경제'
    }
}


news_scraper.main()