import scraperwiki
import mechanize
import lxml.etree
import lxml.html
import re
from httplib import BadStatusLine

#pulls out the pi status and agent status. this data is entered in more effectively on this screen than the basic details
#need to combine this data with the psfscraper

baseurl = "http://www.fsa.gov.uk/register/psdFirmMainSearch.do?" #string
qtwo = "firmName=&"
qfour="postcodeIn=&searchType=1&currAuthorisedInd=on"

pregex=re.compile("(\d+?$)") #precompiled regex for SID extraction

postcodelist =["W1A","W1B","W1C","W1D","W1F","W1G","W1H","W1J","W1K","W1S","W1T","W1U","W1W","W1","W2","W3",
"W4","W5","W6","W7","W8","W9","W10","W11","W12","W13","W14","EC1A","EC1M","EC1N","EC1P","EC1R","EC1V","EC1Y",
"EC2A","EC2M","EC2N","EC2P","EC2R","EC2V","EC2Y","EC3A","EC3M","EC3N","EC3P","EC3R","EC3V","EC4A","EC4M","EC4N",
"EC4P","EC4R","EC4V","EC4Y","SW1A","SW1E","SW1H","SW1P","SW1V","SW1W","SW1X","SW1Y","SW2","SW3","SW4","SW5","SW6",
"SW7","SW8","SW9","SW10","SW11","SW12","SW13","SW14","SW15","SW16","SW17","SW18","SW19","SW20","WC1A","WC1B","WC1E",
"WC1H","WC1N","WC1R","WC1V","WC1X","WC2A","WC2B","WC2E","WC2H","WC2N","WC2R","E20","E18","E1W","E14","E77","E98","E2",
"E1","E3","N1","N1C","SE1","NW1"]

def regFind(str):    
    m=pregex.search(str)
    if m is not None:
        return m.group() # returns matched string - use findall if there are multiple matches

def compileUrl (postcode, pagenumber):
    qone = "pageNumber="+str(pagenumber)+"&"
    qthree="postcodeOut="+postcode+"&"
    targeturl = baseurl+qone+qtwo+qthree+qfour
    return targeturl

def pagenumFind (postcode):
    html = scraperwiki.scrape(compileUrl(postcode, 1))
    root = lxml.html.fromstring(html)
    try:
        mya = root.cssselect("#application-tabs p a")[-1]
        pagenumber = mya.text_content()
    except IndexError:
        pagenumber = 1
    return pagenumber

def grabLinks(postcode, pagenumber):
    try:
        pcount = int(pagenumber)
        for x in xrange(1,pcount+1):
            html = scraperwiki.scrape(compileUrl(postcode, x))
            root = lxml.html.fromstring(html)
            rows = root.cssselect("table.search-results tr")
            xlen = len(rows)
            for x in xrange (1,xlen):
                table_cells = rows[x].cssselect("td")
                hrefs = table_cells[0].cssselect("a")
                record = {}
                record['SID'] = (regFind(hrefs[0].attrib['href']))
                record['Name'] = table_cells[0].text_content()
                record['Postcode'] = postcode
                record['PIStatus'] = table_cells[3].text_content()
                record['AgentStatus'] = table_cells[4].text_content()
                scraperwiki.sqlite.save(['SID'],record,table_name='Firms')

    except ValueError:
        error = "ValueError"
        scraperwiki.sqlite.save(unique_keys=["Postcode"], data={"Postcode":postcode, "Error": error},table_name='Log')
    
    except IndexError:
        error = "IndexError"
        scraperwiki.sqlite.save(unique_keys=["Postcode"], data={"Postcode":postcode, "Error": error},table_name='Log')


try:
    scraperwiki.sqlite.execute("create table Firms (SID string, Name string, Postcode string, PIStatus string, AgentStatus string)")
    scraperwiki.sqlite.execute("create table Log (Postcode string, Error string)")
except:
    print "Table already exists."

for item in postcodelist:
    postcode = item
    pagenumber=pagenumFind(postcode)
    try:
        grabLinks(postcode,pagenumber)
    except BadStatusLine:
        error = "BadStatusLine"
        scraperwiki.sqlite.save(unique_keys=["Postcode"], data={"Postcode": postcode, "Error": error},table_name="Log")
