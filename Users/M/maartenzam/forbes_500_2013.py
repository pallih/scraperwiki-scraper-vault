import scraperwiki
import lxml.html 

rooturl = "http://money.cnn.com/magazines/fortune/global500/2013/full_list/?iid=G500_sp_full"

html = scraperwiki.scrape(rooturl)
          
root = lxml.html.fromstring(html)

for li in root.cssselect("#content-placeholder li"):
    span = li.cssselect("span")
    
    key = span[1].text_content()
    rank = span[0].text_content()
    rev = span[2].text_content()
    prof = span[3].text_content().replace(",", "")
    ass = span[4].text_content()
    revperc = span[5].text_content()
    profperc = span[6].text_content()
    empl = span[7].text_content().replace(",", "")
    equi = int(span[8].text_content().replace(",", "").replace(".0", ""))
    profsal = span[9].text_content()
    profass = span[10].text_content()
    country = span[11].text_content()
    data = {
            'Name' : key,
            'Rank' : rank,
            'Revenue' : rev,
            'Profits' : prof,
            'Assets' : ass,
            'Revenue change' : revperc,
            'Profits change' : profperc,
            'Employees' : empl,
            'Equity' : equi,
            'Profit sales' : profsal,
            'Profit assets' : profass,
            'Country' : country
            }
    scraperwiki.sqlite.save(unique_keys=['Name'], data=data)

import scraperwiki
import lxml.html 

rooturl = "http://money.cnn.com/magazines/fortune/global500/2013/full_list/?iid=G500_sp_full"

html = scraperwiki.scrape(rooturl)
          
root = lxml.html.fromstring(html)

for li in root.cssselect("#content-placeholder li"):
    span = li.cssselect("span")
    
    key = span[1].text_content()
    rank = span[0].text_content()
    rev = span[2].text_content()
    prof = span[3].text_content().replace(",", "")
    ass = span[4].text_content()
    revperc = span[5].text_content()
    profperc = span[6].text_content()
    empl = span[7].text_content().replace(",", "")
    equi = int(span[8].text_content().replace(",", "").replace(".0", ""))
    profsal = span[9].text_content()
    profass = span[10].text_content()
    country = span[11].text_content()
    data = {
            'Name' : key,
            'Rank' : rank,
            'Revenue' : rev,
            'Profits' : prof,
            'Assets' : ass,
            'Revenue change' : revperc,
            'Profits change' : profperc,
            'Employees' : empl,
            'Equity' : equi,
            'Profit sales' : profsal,
            'Profit assets' : profass,
            'Country' : country
            }
    scraperwiki.sqlite.save(unique_keys=['Name'], data=data)

import scraperwiki
import lxml.html 

rooturl = "http://money.cnn.com/magazines/fortune/global500/2013/full_list/?iid=G500_sp_full"

html = scraperwiki.scrape(rooturl)
          
root = lxml.html.fromstring(html)

for li in root.cssselect("#content-placeholder li"):
    span = li.cssselect("span")
    
    key = span[1].text_content()
    rank = span[0].text_content()
    rev = span[2].text_content()
    prof = span[3].text_content().replace(",", "")
    ass = span[4].text_content()
    revperc = span[5].text_content()
    profperc = span[6].text_content()
    empl = span[7].text_content().replace(",", "")
    equi = int(span[8].text_content().replace(",", "").replace(".0", ""))
    profsal = span[9].text_content()
    profass = span[10].text_content()
    country = span[11].text_content()
    data = {
            'Name' : key,
            'Rank' : rank,
            'Revenue' : rev,
            'Profits' : prof,
            'Assets' : ass,
            'Revenue change' : revperc,
            'Profits change' : profperc,
            'Employees' : empl,
            'Equity' : equi,
            'Profit sales' : profsal,
            'Profit assets' : profass,
            'Country' : country
            }
    scraperwiki.sqlite.save(unique_keys=['Name'], data=data)

import scraperwiki
import lxml.html 

rooturl = "http://money.cnn.com/magazines/fortune/global500/2013/full_list/?iid=G500_sp_full"

html = scraperwiki.scrape(rooturl)
          
root = lxml.html.fromstring(html)

for li in root.cssselect("#content-placeholder li"):
    span = li.cssselect("span")
    
    key = span[1].text_content()
    rank = span[0].text_content()
    rev = span[2].text_content()
    prof = span[3].text_content().replace(",", "")
    ass = span[4].text_content()
    revperc = span[5].text_content()
    profperc = span[6].text_content()
    empl = span[7].text_content().replace(",", "")
    equi = int(span[8].text_content().replace(",", "").replace(".0", ""))
    profsal = span[9].text_content()
    profass = span[10].text_content()
    country = span[11].text_content()
    data = {
            'Name' : key,
            'Rank' : rank,
            'Revenue' : rev,
            'Profits' : prof,
            'Assets' : ass,
            'Revenue change' : revperc,
            'Profits change' : profperc,
            'Employees' : empl,
            'Equity' : equi,
            'Profit sales' : profsal,
            'Profit assets' : profass,
            'Country' : country
            }
    scraperwiki.sqlite.save(unique_keys=['Name'], data=data)

