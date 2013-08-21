import scraperwiki
import string


url = 'http://scraperwikiviews.com/run/korean_health_news/'

scrapers = [
    'korean_health_news_scraper_for_chosun',
    'korean_health_news_scraper_for_hankook_i',
    'korean_health_news_scraper_for_donga',
    'korean_health_news_scraper_for_seoul',
    'korean_health_news_scraper_for_joins',
    'korean_health_news_scraper_for_khan',
    'korean_health_news_scraper_for_hani',
    'korean_health_news_scraper_for_munhwa',
    'korean_health_news_scraper_for_money_today',
    'korean_health_news_scraper_for_herald_media',
    'korean_health_news_scraper_for_sports_seoul',
    'korean_health_news_scraper_for_sports_world',
    'korean_health_news_scraper_for_sports_khan',
    'korean_health_news_scraper_for_newdaily',
    'korean_health_news_scraper_for_yonhap_news',
    'korean_health_news_scraper_for_naver'
]


def main():
    global scrapers

    queries = scraperwiki.utils.GET()

    if 'db' not in queries:
        print 'Parameter "db" is missing'
        quit()

    dbs = queries['db'].split(',')
    if len(dbs) > 10:
        print 'Too many DBs'
        quit()

    statements = []
    for db in dbs:
        db = int(db)

        if db < 1 or db > len(scrapers):
            print 'Invalid DB id %d' % db
            quit()

        scraperwiki.sqlite.attach(scrapers[db-1])
        statements.append("SELECT source, date, title FROM %s.swdata" % scrapers[db-1])

    statements = " UNION ".join(statements) + " GROUP BY title ORDER BY date DESC"
    if 'page' in queries and 'count' in queries:
        page        = int(queries['page']) - 1
        count       = int(queries['count'])
        statements += " LIMIT %d, %d" % (count * page, count)

    data = scraperwiki.sqlite.execute(statements)
    data = [ dict(zip(data['keys'], record)) for record in data['data'] ]

    print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"'
    print ' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
    print '<html xmlns="http://www.w3.org/1999/xhtml">'
    print '<head>'
    print '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    print '  <title>Korean Health News</title>'
    print '  <style type="text/css">'
    print '    body {'
    print '      font-family      : verdana, helvetica, arial, sans-serif;'
    print '      font-size        : 100%;'
    print '      color            : #000000;'
    print '      background-color : #FFFFFF;'
    print '    }'
    print '    table {'
    print '      color            : #000000;'
    print '      background-color : #FFFFFF;'
    print '      border           : 1px solid #C3C3C3;'
    print '      border-collapse  : collapse;'
    print '    }'
    print '    thead {'
    print '      color            : #000000;'
    print '      background-color : #E5EECC;'
    print '      border           : 1px solid #C3C3C3;'
    print '      padding          : 3px;'
    print '      vertical-align   : top;'
    print '    }'
    print '    td {'
    print '      border         : 1px solid #C3C3C3;'
    print '      padding        : 3px;'
    print '      vertical-align : top;'
    print '    }'
    print '  </style>'
    print '</head>'
    print '<body>'
    print '  <table>'
    print '    <thead>'
    print '      <tr><th>출처</th><th>날짜</th><th>제목</th></tr>'
    print '    </thead>'
    print '    <tbody>'
    for article in data:
        print '      <tr>'
        print '        <td>', article['source'], '</td>'
        print '        <td>', article['date'], '</td>'
        print '        <td>', article['title'], '</td>'
        print '      </tr>'
    print '    </tbody>'
    print '  </table>'
    print '</body>'
    print '</html>'


main()