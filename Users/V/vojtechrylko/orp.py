import scraperwiki
import lxml.html
from lxml import etree

YEARS = range(2002, 2012)


class ORPScraper:
    URL = "http://isoh.cenia.cz/groupisoh/orp.php?rok="
    
    def __init__(self, db):
        scraperwiki.sqlite.execute("create table if not exists " + db + "(year int, code int, name varchar)")
        self._commit()
        self._db = db
        

    def scrap(self, year):
        html = scraperwiki.scrape(ORPScraper.URL + str(year))
        tree = lxml.html.fromstring(html)
        rows = tree.xpath('//table[@class="Normal"]/tr')
        for row in rows:
            #print etree.tostring(row)
            code = row.xpath('td[1]/b/text()')
            if not code:
                # 'filter' header
                continue
            icode = int(code[0])
            name = row.xpath('td[2]/a/text()')
            assert name
            sname = name[0]
            scraperwiki.sqlite.execute("insert into " + self._db + "(year, code, name) values (?,?,?)", (year, icode, sname))
        self._commit()


    def _commit(self):
        scraperwiki.sqlite.commit()
        

scraper = ORPScraper('orp')
for year in YEARS:
    print year
    scraper.scrap(year)
        
        
    import scraperwiki
import lxml.html
from lxml import etree

YEARS = range(2002, 2012)


class ORPScraper:
    URL = "http://isoh.cenia.cz/groupisoh/orp.php?rok="
    
    def __init__(self, db):
        scraperwiki.sqlite.execute("create table if not exists " + db + "(year int, code int, name varchar)")
        self._commit()
        self._db = db
        

    def scrap(self, year):
        html = scraperwiki.scrape(ORPScraper.URL + str(year))
        tree = lxml.html.fromstring(html)
        rows = tree.xpath('//table[@class="Normal"]/tr')
        for row in rows:
            #print etree.tostring(row)
            code = row.xpath('td[1]/b/text()')
            if not code:
                # 'filter' header
                continue
            icode = int(code[0])
            name = row.xpath('td[2]/a/text()')
            assert name
            sname = name[0]
            scraperwiki.sqlite.execute("insert into " + self._db + "(year, code, name) values (?,?,?)", (year, icode, sname))
        self._commit()


    def _commit(self):
        scraperwiki.sqlite.commit()
        

scraper = ORPScraper('orp')
for year in YEARS:
    print year
    scraper.scrap(year)
        
        
    