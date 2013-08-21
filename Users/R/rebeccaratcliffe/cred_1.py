                                                                     
                                                                     
                                                                     
                                             
import scraperwiki

# Blank Python

# typical URL is http://www.london-gazette.co.uk/id/issues/60112/notices/1568529
# list of URLs collected by scraper at https://scraperwiki.com/scrapers/bankruptcies/
# Downloaded as CSV and codes extracted in Google Docs by using =RIGHT(A2, 7)
# Cycle through a list of those codes, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url'

import scraperwiki
#import urlparse
import lxml.html
from lxml import etree

#TM - set debug on or off
debug = False

# search for a span property by XPath
def search_by_span_attribute(root, attribute, value):
    foundVal = root.xpath("//span[@" + attribute + "='" + value + "']")
    if foundVal:
        if debug:
            print attribute + " " + value + " found with text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print attribute + " not found."
        return ""

# custom search
def search_xpath(root, xpath):
    foundVal = root.xpath(xpath)
    if foundVal:
        if debug:
            print xpath + " returned text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print xpath + " returned no results found."
        return ""

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Create a new empty record
    record = {}

    record['pubdate'] = search_by_span_attribute(root, "property", "g:hasPublicationDate")
    record['noticecode'] = search_by_span_attribute(root, "property", "g:hasNoticeCode")
    #TM - you'll need to look for an example of this from page source when you come across one that should have it... unless it is the same as court:courtName below?
    #record['registry'] = search_by_span_attribute(root, "property",
    record['company number'] = search_by_span_attribute(root, "property", "organisation:companyNumber")
    record['company name'] = search_by_span_attribute(root, "property", "organisation:name")
    record['nature of business'] = search_by_span_attribute(root, "property", "organisation:natureOfBusiness")
    #record['trade classification'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    #TM - this one is a bit special as there are two that match it if you search for just the "vCard:label" property. To guarantee the right one, we have to customize the XPath a bit...
    record['registered office of company'] = search_xpath(root, "//span[@rel='organisation:hasRegisteredOffice']//span[@property='vCard:label']")
    #record['sector'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    record['court'] = search_by_span_attribute(root, "property", "court:courtName")
    #record['date'] = search_by_span_attribute(root, "property", #same as date?
    #record['urlcode'] = search_by_span_attribute(root, "property",
    record['ID'] = item

    scraperwiki.sqlite.save(["ID"], record)
       

#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    #TM - commented out the below print
    #print html
    #now we use the lxml.html function imported above to convert 'html' into a new object, 'root'
    #TM - except we are now using etree!
    #root = lxml.html.fromstring(html)
    root = etree.HTML(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://www.london-gazette.co.uk/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes =['60408/notices/1755257','60413/notices/1757228','60418/notices/1760172','60419/notices/1762318','60427/notices/1767800','60428/notices/1767150','60408/notices/1753934','60408/notices/1753936','60408/notices/1755256','60408/notices/1753359','60408/notices/1753904','60409/notices/1754729','60409/notices/1754726','60409/notices/1754394','60409/notices/1754153','60411/notices/1757510','60411/notices/1757135','60411/notices/1755288','60411/notices/1755289','60411/notices/1755798','60412/notices/1756755','60412/notices/1756027','60412/notices/1756165','60413/notices/1757006','60413/notices/1757008','60413/notices/1759046','60413/notices/1757854','60413/notices/1757819','60413/notices/1757840','60414/notices/1758355','60414/notices/1757930','60414/notices/1758954','60415/notices/1759161','60415/notices/1759774','60418/notices/1760696','60418/notices/1760692','60418/notices/1761569','60419/notices/1761199','60419/notices/1763536','60419/notices/1761956','60419/notices/1761213','60420/notices/1764432','60420/notices/1764433','60420/notices/1762382','60420/notices/1762967','60420/notices/1762968','60420/notices/1763007','60420/notices/1762376','60420/notices/1762635','60420/notices/1762366','60422/notices/1762888','60422/notices/1763634','60422/notices/1765245','60422/notices/1765196','60422/notices/1764104','60422/notices/1763439','60423/notices/1766274','60423/notices/1765965','60423/notices/1764381','60423/notices/1764915','60426/notices/1765057','60426/notices/1765918','60426/notices/1765877','60426/notices/1766806','60426/notices/1765917','60426/notices/1764998','60427/notices/1766925','60427/notices/1766922','60427/notices/1766929','60427/notices/1766288','60428/notices/1767152','60428/notices/1767660','60429/notices/1767999','60429/notices/1768540','60429/notices/1768529','60430/notices/1769789','60430/notices/1770207','60430/notices/1769796','60433/notices/1770531','60433/notices/1770520','60433/notices/1771050','60433/notices/1770228','60433/notices/1770500','60435/notices/1772009','60435/notices/1772373','60435/notices/1771899','60435/notices/1772438','60435/notices/1771923','60436/notices/1773327','60436/notices/1773340','60436/notices/1773381','60436/notices/1773307','60408/notices/1753906','60408/notices/1754175','60408/notices/1753980','60408/notices/1753948','60408/notices/1753343','60409/notices/1755125','60409/notices/1755126','60409/notices/1754689','60411/notices/1755779','60411/notices/1755796','60411/notices/1755789','60411/notices/1757136','60412/notices/1755862','60412/notices/1755999','60413/notices/1757806','60413/notices/1757826','60413/notices/1758192','60413/notices/1758193','60414/notices/1759363','60414/notices/1759013','60414/notices/1759364','60414/notices/1758876','60415/notices/1759823','60415/notices/1759829','60415/notices/1759145','60415/notices/1759792','60415/notices/1759804','60415/notices/1759787','60415/notices/1759922','60415/notices/1759826','60418/notices/1760680','60418/notices/1760636','60419/notices/1761936','60419/notices/1761200','60419/notices/1761927','60419/notices/1761181','60420/notices/1763015','60420/notices/1763961','60422/notices/1765195','60423/notices/1764380','60423/notices/1766273','60423/notices/1765516','60423/notices/1764882','60423/notices/1764884','60426/notices/1767054','60426/notices/1765884','60426/notices/1765939','60427/notices/1766903','60427/notices/1766936','60427/notices/1766866','60427/notices/1767131','60428/notices/1767151','60428/notices/1767745','60428/notices/1767657','60428/notices/1767733','60429/notices/1768010','60429/notices/1768009','60429/notices/1768861','60429/notices/1769887','60429/notices/1769888','60429/notices/1768595','60430/notices/1769407','60430/notices/1770763','60430/notices/1770208','60430/notices/1770209','60433/notices/1770529','60433/notices/1771844','60433/notices/1771845','60433/notices/1770415','60436/notices/1773085','60436/notices/1772656','60436/notices/1772657','60436/notices/1773373','60436/notices/1773354','60436/notices/1773313','60436/notices/1773328','60408/notices/1754190','60409/notices/1756118','60419/notices/1761147','60420/notices/1764423']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)



