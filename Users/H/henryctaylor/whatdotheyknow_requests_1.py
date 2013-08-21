import scraperwiki
import csv
import lxml.html

from time import sleep

def getBodies():
    data = scraperwiki.scrape('http://www.whatdotheyknow.com/body/all-authorities.csv')
    try: scraperwiki.sqlite.execute('DELETE FROM bodies')
    except:pass
    try:scraperwiki.sqlite.execute('DELETE FROM tags')
    except:pass

    rdr = csv.DictReader(data.splitlines())

    tags = []
    bodies = []
    for row in rdr:
        for tag in row['Tags'].split():
            (tagname, _, value) = tag.partition(':')
            tags += [{ 'Tag': tagname, 'Value': value, 'URLname': row['URL name'] }]
        del row['Tags']
        bodies.append(row)

    scraperwiki.sqlite.save(['URL name'], bodies, table_name='bodies')
    scraperwiki.sqlite.save(['Tag', 'Value', 'URLname'], tags, table_name = 'tags')

    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS body_byurl ON bodies (`URLname`)')
    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS body_byname ON bodies (`Name`)')
    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS tag_bytag ON tags(`Tag`)')
    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS tag_byurl ON tags(`URLname`)')
    scraperwiki.sqlite.execute('ANALYZE')
    scraperwiki.sqlite.commit()

#getBodies()

def getXLSSearchPage(ccl, page=1):
    scraping=1
    results=[]
    while scraping==1:
        url='http://www.whatdotheyknow.com/search/filetype:xls%20requested_from:'+ccl+'/all?page='+str(page)
        #url='http://www.whatdotheyknow.com/search/requested_from:'+ccl+'/all?page='+str(page)
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        for item in root.cssselect("span.head a"):
            href= item.get('href')
            if href not in grabbed:
                record={}
                record['body']=ccl
                record['requestPath']=href
                record['requestTitle']=item.text
                print record
                scraperwiki.sqlite.save(['requestPath'], record, table_name=tn)
        if len(root.cssselect("a.next_page")):
            print 'grabbing another results page',str(page)
            page=page+1
        else:
            print 'done that...'
            scraping=0
    return




typs=['local_council']
for typ in typs:
    if typ=='nhs_trust':  tn='xlsReturns_nhsTrust_and_PCT'
    else: tn='xlsReturns_'+typ
    try: grabbed=scraperwiki.sqlite.select("requestPath from "+tn)
    except:grabbed=[]
    #typ2='parish_council'
    #getXLSSearchPage('kent_county_council')
    q = '* FROM "tags" where Tag=="'+typ+'"'
    #q = '* FROM "tags"'
    data = scraperwiki.sqlite.select(q)
    print data
    for item in data:
        print item['URLname']
        getXLSSearchPage(item['URLname'])
        sleep(0.5)
#http://www.whatdotheyknow.com/search/filetype:xls%20requested_from:kent_county_council/all
#(filetype:xlsx OR filetype:xlsx) requested_from:kent_county_council