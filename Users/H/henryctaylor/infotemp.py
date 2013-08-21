                                             



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
    record['registered office address of company'] = search_by_span_attribute(root, "property", "organisation:hasOffice")
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
codes=['60428/notices/1769022','60429/notices/1770052','60429/notices/1768521','60429/notices/1770053','60429/notices/1768579','60429/notices/1769890','60429/notices/1770054','60429/notices/1769582','60429/notices/1768862','60429/notices/1767977','60429/notices/1767990','60429/notices/1770055','60429/notices/1767971','60429/notices/1768576','60430/notices/1769805','60430/notices/1768923','60430/notices/1769813','60430/notices/1769435','60430/notices/1769763','60430/notices/1768937','60430/notices/1769436','60430/notices/1768932','60430/notices/1770827','60430/notices/1770828','60433/notices/1769958','60433/notices/1770260','60433/notices/1771809','60433/notices/1771810','60433/notices/1771444','60433/notices/1769910','60433/notices/1770557','60433/notices/1771846','60433/notices/1769933','60433/notices/1770496','60433/notices/1770512','60433/notices/1769922','60433/notices/1770467','60434/notices/1771699','60434/notices/1771689','60434/notices/1772838','60434/notices/1771691','60434/notices/1771650','60434/notices/1771652','60434/notices/1771707','60434/notices/1772935','60434/notices/1771765','60434/notices/1772936','60434/notices/1771683','60434/notices/1772937','60434/notices/1772938','60434/notices/1771262','60434/notices/1772673','60434/notices/1771654','60434/notices/1772839','60434/notices/1771714','60435/notices/1773790','60435/notices/1773613','60435/notices/1771927','60435/notices/1772420','60435/notices/1772065','60435/notices/1773704','60435/notices/1773791','60435/notices/1772390','60435/notices/1773657','60435/notices/1773792','60435/notices/1771915','60435/notices/1773793','60435/notices/1771924','60435/notices/1772363','60435/notices/1772078','60435/notices/1771907','60435/notices/1771930','60435/notices/1771901','60382/notices/1737972','60393/notices/1743583','60394/notices/1745620','60395/notices/1746401','60399/notices/1748043','60400/notices/1746345','60400/notices/1746346','60400/notices/1746347','60400/notices/1746348','60400/notices/1746349','60400/notices/1746350','60400/notices/1746351','60400/notices/1746352','60400/notices/1746353','60400/notices/1746354','60400/notices/1746355','60400/notices/1746356','60400/notices/1746357','60400/notices/1746358','60400/notices/1746359','60400/notices/1746360','60400/notices/1746361','60400/notices/1746362','60400/notices/1746363','60400/notices/1746364','60401/notices/1749613','60401/notices/1749614','60403/notices/1751431','60403/notices/1751432','60403/notices/1751433','60405/notices/1752530','60406/notices/1750417','60406/notices/1750418','60406/notices/1750419','60406/notices/1750420','60406/notices/1750421','60406/notices/1750422','60406/notices/1750423','60406/notices/1750424','60406/notices/1750425','60406/notices/1750426','60406/notices/1752934','60406/notices/1750427','60406/notices/1750428','60406/notices/1750429','60406/notices/1750430','60406/notices/1750431','60406/notices/1750432','60406/notices/1750433','60406/notices/1750434','60409/notices/1756810','60411/notices/1757529','60411/notices/1755069','60412/notices/1755881','60412/notices/1755882','60412/notices/1755883','60412/notices/1755884','60412/notices/1755885','60412/notices/1755886','60412/notices/1755887','60412/notices/1755888','60412/notices/1755889','60412/notices/1755890','60412/notices/1755891','60412/notices/1755892','60412/notices/1755893','60412/notices/1755894','60412/notices/1755895','60414/notices/1759976','60415/notices/1761281','60419/notices/1759028','60419/notices/1759029','60419/notices/1759030','60419/notices/1759031','60419/notices/1759032','60419/notices/1763882','60419/notices/1759033','60419/notices/1759034','60419/notices/1759035','60422/notices/1765209','60423/notices/1766579','60423/notices/1766580','60427/notices/1766000','60427/notices/1766001','60427/notices/1766002','60427/notices/1766003','60427/notices/1766004','60427/notices/1766005','60427/notices/1766006','60428/notices/1769058','60430/notices/1771209','60434/notices/1770768','60434/notices/1770769','60434/notices/1770770','60434/notices/1770771','60434/notices/1770772','60434/notices/1770773','60408/notices/1754771','60411/notices/1756480','60411/notices/1756479','60426/notices/1766659','60434/notices/1772202']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)
