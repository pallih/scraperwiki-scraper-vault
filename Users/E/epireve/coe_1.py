import scraperwiki
import mechanize
import lxml.html
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import re

def scrape_table(root):
    #root = BeautifulSoup(''.join(root))
    print root.prettify()
    idno = 0
    record = {}
    nric = ""
    name = ""
    sex = ""
    bdate = ""
    parliament = ""
    state = ""
    
    nric = root.find('span', id="LabelIC").string
    name = root.find('span', id="Labelnama").string
    sex = root.find('span', id="Labeljantina").string
    bdate = root.find('span', id="LabelTlahir").string
    parliament = root.find('span', id="Labelpar").string
    state = root.find('span', id="Labelnegeri").string
    
    idno += 1
    record['Index'] = idno
    record['ID Number'] = nric
    record['Name'] = name

    if sex == "LELAKI": record['Sex'] = "MALE"
    else: record['Sex'] = "FEMALE"
        
    record['Birthday'] = bdate
    record['Parliament'] = parliament
    record['State'] = state
    #find any links <a ...
    #table_cellsurls = table_cells[0].cssselect("a")
    #grab the href=" attribute of the first <a ... and store
    #record['URL'] = table_cellsurls[0].attrib.get('href')
        # Print out the data we've gathered
    print record, '------------'
    scraperwiki.sqlite.save(["ID Number"], record)
    
starting_url = 'http://daftarj.spr.gov.my/NEWDAFTARJ'
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(starting_url)
print "All forms:", [ form.name for form in br.forms() ]
br.select_form(name="def")

for num in range(5500,5600):
    NumIC = '90121611'+str(num)
    #print NumIC
    br["txtIC"] = "901216115519"
    response = br.submit()
    html = response.read()
    response = br.response()
    response.read()
    root = BeautifulSoup(''.join(html))
    gotdata = root.find('span', id="LabelIC").string
    if gotdata: # <script language="javascript" type="text/javascript">alert('Record not found.');</script>
        scrape_table(root)

#br["txtIC"] = "900813146650"
#response = br.submit()
#html = response.read()
#print html
#root = lxml.html.fromstring(html)


