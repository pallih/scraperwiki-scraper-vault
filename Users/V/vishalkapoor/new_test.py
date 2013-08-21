import scraperwiki
from BeautifulSoup import BeautifulSoup

def display(o):
    scraperwiki.metadata.save('data_columns', ['Details','Type','Readers','Percentage of readers'])
    tbl = o.find("table", {"class": "in-article sortable"})
    
    rows = tbl.findAll("tr")
    for row in rows:
        record = {}
        
        cols = row.findAll("td")
        
        if len(cols) == 4:
            record['Details'] = cols[0].text
            record['Type'] = cols[1].text
            record['Readers'] = cols[2].text
            record['Percentage of readers'] = cols[3].text
            print record,
            print "-------------"
            
            scraperwiki.datastore.save(["Details"], record)



db="http://www.guardian.co.uk/news/datablog/2011/jul/08/news-of-the-world-circulation-data"
getdata=scraperwiki.scrape(db)
o = BeautifulSoup(getdata)
display(o)

