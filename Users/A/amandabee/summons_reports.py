from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring,tostring

url = "http://www.nyc.gov/html/nypd/html/traffic_reports/traffic_summons_reports.shtml"


## Based on https://scraperwiki.com/scrapers/jdnyc_stream_c_python_1/edit/ I should 
## define columns, but https://scraperwiki.com/docs/python/python_intro_tutorial/ says 
## I don't need to. 

## the example from the workshop is crazy unhelpful because it ends up with all 
## these cockamamie names and if you're not intimate with Python it's hard to know 
## what's a command and whats foo.


nypd_html = scrape(url)
nypd_page = fromstring(nypd_html)
    
nypd_crux = nypd_page.cssselect("span.bodytext")[2] 

print nypd_crux;

for text in nypd_crux.csssleect("p b a"):
    nypd_boro = text
    data = {
        'boro' : nypd_boro
    }

    print data
    scraperwiki.sqlite.save(unique_keys=['boro'], data=data)




