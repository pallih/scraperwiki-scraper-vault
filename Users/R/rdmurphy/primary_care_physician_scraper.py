import scraperwiki
import lxml.html
import os, cgi

qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))

print qsenv["ACCESS_KEY"]

BASE_URL = "http://www.dshs.state.tx.us/chs/hprc/tables/"

SCRAPE_TARGETS = { 2001 : "01PC.shtm",
                   2002 : "02PC.shtm",
                   2003 : "03PC.shtm", 
                   2004 : "04PC.shtm",
                   2005 : "05PC.shtm",
                   2006 : "06PC.shtm",
                   2007 : "07PC.shtm",
                   2008 : "08PC.shtm",
                   2009 : "09PC.shtm",
                   2010 : "Primary-Care-Physicians-(PC)-by-County-of-Practice---September,-2010/",
                   2011 : "Primary-Care-Physicians-(PC)-by-County-of-Practice---September,-2011/"
}


datastore = {}

for year in SCRAPE_TARGETS:
    print "Starting", year
    url = BASE_URL + SCRAPE_TARGETS[year]
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    if year < 2010:
        if year == 2009:
            content = root.cssselect("table.content")[0].cssselect("tr")
        else:
            content = root.cssselect("table.content tr")
    else:
        content = root.cssselect("table.border tr")
    content = content[1:]

    for entry in content:
        county = entry.cssselect("td")[0].text_content().strip()
        pop = int((entry.cssselect("td")[1].text_content().strip()).replace(",",""))
        pc = int((entry.cssselect("td")[2].text_content().strip()).replace(",",""))
        
        if county not in datastore:
            datastore[county] = {}
        pop_entry = "pop" + str(year)
        pc_entry = "pc" + str(year)
        datastore[county].update({pop_entry : pop})
        datastore[county].update({pc_entry : pc})

    print year, "finished"

print datastore

payload = []

for entry in datastore:
    temp = {}
    temp["county"] = entry
    temp.update(datastore[entry])
    payload.append(temp)

scraperwiki.sqlite.save(["county"], data=payload)
    
        


