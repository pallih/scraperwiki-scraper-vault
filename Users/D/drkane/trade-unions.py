###############################################################################
# Trade Unions scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import time

# retrieve a page
starting_url = 'http://www.certoffice.org/Nav/Trade-Unions/Active.aspx?dlcats='
dlcats = ['2','3']
for dlcat in dlcats:
    html = scraperwiki.scrape(starting_url + dlcat)
    #print html
    soup = BeautifulSoup(html)
    
    # use BeautifulSoup to get all <td> tags
    table = soup.findAll('table')
    trs = table[2].findAll('tr') 
    for tr in trs:
        tds = tr.findAll('td')
        name = tds[2].contents[0]
        try:
            website = tds[1].findAll('a')[0]['href']
        except:
            website = ''
        try:
            moreinfo = 'http://www.certoffice.org' + tds[2].findAll('a')[0]['href']
            reports = scraperwiki.scrape(moreinfo)
            reportsoup = BeautifulSoup(reports)
            latestreport = 'http://www.certoffice.org' + reportsoup.find('div', 'content-lower-news-listing').find('div').find('a')['href']
        except:
            moreinfo = ''
            latestreport = ''
        if dlcat=='2':
            scheduled = "false"
        else:
            scheduled = "true"
        print name, website, latestreport, moreinfo, scheduled
        record = { "name" : name , "website" : website , "latestreport" : latestreport, "moreinfo" : moreinfo, "scheduled" : scheduled }
        # save records to the datastore
        scraperwiki.sqlite.save(["name"], record) 