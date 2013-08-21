import scraperwiki
import BeautifulSoup
import re

index_url = "http://www.afp.gov.au/about-the-afp/accountability-requirements/harradine-report.aspx"

def page(link):
    html = scraperwiki.scrape(link)
    soup = BeautifulSoup.BeautifulSoup(html)
    table = soup.find('table')
    rows = table.findAll('tr')
    name = []
    for th in rows[0].findAll('th'):
        if th.string == "Prefix:":
            name.append("prefix")
        elif re.search(r'file\s+no', th.string, re.IGNORECASE):
            name.append("file_no")
        elif re.search('part', th.string, re.IGNORECASE):
            name.append("part_no")
        elif th.string == "Function:":
            name.append("function")
        elif th.string == "Activity:":
            name.append("activity")
        elif re.search(r'title', th.string, re.IGNORECASE):
            name.append("title")
        else:
            name.append("unknown")
            print "Could not recognise header value " + th.string
    for row in rows[1:-1]:
        tds = row.findAll('td')
        data = dict(zip(name, (td.string for td in tds)))
        if data["file_no"] is None:
            #print "skipped blank row"
            continue
        #print data["file_no"]
        scraperwiki.datastore.save(["file_no"], data)
        
html = scraperwiki.scrape(index_url)
soup = BeautifulSoup.BeautifulSoup(html)
link_tags = soup.find('div', {"class" : "contentModule"}).findAll("a")

for tag in link_tags:
    page("http://www.afp.gov.au" + tag['href'])
