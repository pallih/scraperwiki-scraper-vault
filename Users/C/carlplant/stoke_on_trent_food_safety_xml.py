import scraperwiki
import mechanize
import urlparse
import lxml.html
import re
import lxml.etree


url = 'http://ratings.food.gov.uk/search/en-GB?ba=stoke+on+trent&sm=1&st=1&pi=0&sc=%2fsearch%2fen-GB'
br = mechanize.Browser()

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

for pagenum in range(10):
    html = response.read()
    print "Page %d  page length %d" % (pagenum, len(html))
    #print "Clinicians found:", re.findall("PDetails.aspx\?ProviderId.*?>(.*?)</a>", html)

    mnextlink = re.search("Next &gt;", html) 
    print mnextlink
    if not mnextlink:
        break
    
    br.select_form(name='ctl00$ContentPlaceHolder1$uxResults$lnkNext')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'Next'
    br['__EVENTARGUMENT'] = ''
    response = br.submit()

    print html

root = lxml.html.fromstring(html)
#print lxml.etree.tostring(root)
print "All forms:", [ form.name  for form in br.forms() ]

#def scrape_table(root):
rows = root.cssselect("table.uxMainResults.ShowMap tr")  # selects all <tr> blocks within <table class="uxMain Results">
for row in rows:
        # Set up our data record - we'll need it later
    record = {}
    table_cells = row.cssselect("div")
    if table_cells: 
        record['Address'] = table_cells[3].text
        record['Inspection date'] = table_cells[5].text
        record['Lat'] = table_cells[6].text
        record['Lng'] = table_cells[7].text
    table_cells2 = row.cssselect("div.resultName a")
    if table_cells2:
        record['Name'] = table_cells2[0].text
        print record, '------------'   
        scraperwiki.sqlite.save(["Name"], record)





