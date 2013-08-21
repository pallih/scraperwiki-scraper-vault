                                                                     
                                                                     
                                                                     
                                             
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
codes =['60379/notices/1736224','60379/notices/1736230','60379/notices/1736225','60379/notices/1736228','60379/notices/1736231','60379/notices/1736229','60379/notices/1736227','60379/notices/1736226','60380/notices/1736699','60380/notices/1736700','60381/notices/1737148','60381/notices/1737147','60382/notices/1737926','60382/notices/1737923','60382/notices/1737922','60382/notices/1737921','60382/notices/1737927','60382/notices/1737925','60382/notices/1737924','60384/notices/1738307','60384/notices/1738304','60384/notices/1738306','60384/notices/1738303','60384/notices/1738309','60384/notices/1738308','60384/notices/1738302','60384/notices/1738305','60385/notices/1739176','60385/notices/1739179','60385/notices/1739175','60385/notices/1739180','60385/notices/1739178','60385/notices/1739177','60386/notices/1740319','60386/notices/1740315','60386/notices/1740314','60386/notices/1740316','60386/notices/1740312','60386/notices/1740317','60386/notices/1740318','60386/notices/1740313','60389/notices/1741119','60389/notices/1741125','60389/notices/1741128','60389/notices/1741122','60389/notices/1741123','60389/notices/1741121','60389/notices/1741115','60389/notices/1741117','60389/notices/1741120','60389/notices/1741127','60389/notices/1741126','60389/notices/1741118','60389/notices/1741124','60389/notices/1741116','60390/notices/1742150','60390/notices/1742145','60390/notices/1742146','60390/notices/1742149','60390/notices/1742148','60390/notices/1742152','60390/notices/1742153','60390/notices/1742151','60390/notices/1742147','60390/notices/1742144','60392/notices/1743067','60392/notices/1743069','60392/notices/1743072','60392/notices/1743071','60392/notices/1743068','60392/notices/1743070','60392/notices/1743073','60393/notices/1744508','60393/notices/1744509','60393/notices/1744512','60393/notices/1744510','60393/notices/1744511','60394/notices/1744934','60394/notices/1744932','60394/notices/1744933','60395/notices/1745846','60395/notices/1745845','60396/notices/1746754','60396/notices/1746746','60396/notices/1746748','60396/notices/1746756','60396/notices/1746758','60396/notices/1746744','60396/notices/1746749','60396/notices/1746743','60396/notices/1746750','60396/notices/1746755','60396/notices/1746751','60396/notices/1746741','60396/notices/1746753','60396/notices/1746742','60396/notices/1746752','60396/notices/1746745','60396/notices/1746757','60396/notices/1746747','60399/notices/1747766','60399/notices/1747775','60399/notices/1747780','60399/notices/1747755','60399/notices/1747781','60399/notices/1747776','60399/notices/1747773','60399/notices/1747748','60399/notices/1747774','60399/notices/1747753','60399/notices/1747765','60399/notices/1747769','60399/notices/1747771','60399/notices/1747757','60399/notices/1747761','60399/notices/1747772','60399/notices/1747747','60399/notices/1747782','60399/notices/1747764','60399/notices/1747777','60399/notices/1747779','60399/notices/1747770','60399/notices/1747768','60399/notices/1747745','60399/notices/1747749','60399/notices/1747763','60399/notices/1747767','60399/notices/1747778','60399/notices/1747746','60399/notices/1747759','60399/notices/1747751','60400/notices/1748548','60400/notices/1748546','60400/notices/1748551','60400/notices/1748553','60400/notices/1748552','60400/notices/1748549','60400/notices/1748555','60400/notices/1748550','60400/notices/1748557','60400/notices/1748554','60400/notices/1748547','60400/notices/1748556','60401/notices/1749141','60401/notices/1749142','60401/notices/1749143','60401/notices/1749144','60401/notices/1749140','60401/notices/1749138','60401/notices/1749139','60402/notices/1750575','60402/notices/1750182','60402/notices/1750173','60402/notices/1750174','60402/notices/1750180','60402/notices/1750176','60402/notices/1750183','60402/notices/1750181','60402/notices/1750175','60402/notices/1750177','60402/notices/1750179','60402/notices/1750178','60403/notices/1751493','60403/notices/1751485','60403/notices/1751489','60403/notices/1751495','60403/notices/1751491','60403/notices/1751488','60403/notices/1751498','60403/notices/1751492','60403/notices/1751481','60403/notices/1751497','60403/notices/1751500','60403/notices/1751482','60403/notices/1751496','60403/notices/1751504','60403/notices/1751475','60403/notices/1751477','60403/notices/1751476','60403/notices/1751473','60403/notices/1751478','60403/notices/1751474','60403/notices/1751503','60403/notices/1751487','60403/notices/1751483','60403/notices/1751494','60403/notices/1751490','60403/notices/1751486','60403/notices/1751499','60403/notices/1751480','60403/notices/1751502','60403/notices/1751479','60403/notices/1751484','60403/notices/1751501','60405/notices/1752033','60405/notices/1752036','60405/notices/1752049','60405/notices/1752056','60405/notices/1752045','60405/notices/1752035','60405/notices/1752034','60405/notices/1752044','60405/notices/1752024','60405/notices/1752037','60405/notices/1752040','60405/notices/1752054','60405/notices/1752038','60405/notices/1752050','60405/notices/1752046','60405/notices/1752027','60405/notices/1752030','60405/notices/1752051','60405/notices/1752041','60405/notices/1752055','60405/notices/1752053','60405/notices/1752031','60405/notices/1752039','60405/notices/1752029','60405/notices/1752362','60405/notices/1752048','60405/notices/1752052','60405/notices/1752043','60405/notices/1752047','60405/notices/1752026','60405/notices/1752042','60405/notices/1752025','60405/notices/1752028','60405/notices/1752032','60406/notices/1752965','60406/notices/1752956','60406/notices/1752950','60406/notices/1752966','60406/notices/1752961','60406/notices/1752958','60406/notices/1752967','60406/notices/1752952','60406/notices/1752962','60406/notices/1752957','60406/notices/1752949','60406/notices/1752960','60406/notices/1752954','60406/notices/1752964','60406/notices/1752969','60406/notices/1752951','60406/notices/1752948','60406/notices/1752959','60406/notices/1752955','60406/notices/1752968','60406/notices/1752953','60406/notices/1752963','60407/notices/1753561','60407/notices/1753565','60407/notices/1753564','60407/notices/1753574','60407/notices/1753567','60407/notices/1753562','60407/notices/1753566','60407/notices/1753568','60407/notices/1753563','60407/notices/1753573','60407/notices/1753570','60407/notices/1753572','60407/notices/1753571','60407/notices/1753569','60408/notices/1754766','60408/notices/1754765','60408/notices/1754769','60408/notices/1754767','60408/notices/1754770','60408/notices/1754764','60408/notices/1754768','60409/notices/1755578','60409/notices/1755567','60409/notices/1755569','60409/notices/1755568','60409/notices/1755575','60409/notices/1755574','60409/notices/1755595','60409/notices/1755577','60409/notices/1755570','60409/notices/1755589','60409/notices/1755596','60409/notices/1755582','60409/notices/1755572','60409/notices/1755597','60409/notices/1755586','60409/notices/1755598','60409/notices/1755600','60409/notices/1755590','60409/notices/1755591','60409/notices/1755599','60409/notices/1755584','60409/notices/1755587','60409/notices/1755588','60409/notices/1755573','60409/notices/1755581','60409/notices/1755580','60409/notices/1755594','60409/notices/1755562','60409/notices/1755576','60409/notices/1755571','60409/notices/1755563','60409/notices/1755564','60409/notices/1755592','60409/notices/1755585','60409/notices/1755593','60409/notices/1755579','60409/notices/1755566','60409/notices/1755565','60409/notices/1755583','60411/notices/1756477','60411/notices/1756451','60411/notices/1756476','60411/notices/1756465','60411/notices/1756461','60411/notices/1756467','60411/notices/1756472','60411/notices/1756473','60411/notices/1756456','60411/notices/1756475','60411/notices/1756464','60411/notices/1756463','60411/notices/1756466','60411/notices/1756474','60411/notices/1756460','60411/notices/1756459','60411/notices/1756470','60411/notices/1756452','60411/notices/1756453','60411/notices/1756471','60411/notices/1756457','60411/notices/1756454','60411/notices/1756469','60411/notices/1756450','60411/notices/1756468','60411/notices/1756478','60411/notices/1756455','60411/notices/1756458','60411/notices/1756462','60412/notices/1758068','60412/notices/1758067','60412/notices/1758072','60412/notices/1758065','60412/notices/1758077','60412/notices/1758071','60412/notices/1758066','60412/notices/1758070','60412/notices/1758078','60412/notices/1758073','60412/notices/1758063','60412/notices/1758074','60412/notices/1758069','60412/notices/1758064','60412/notices/1758075','60412/notices/1758076','60413/notices/1758698','60413/notices/1758697','60413/notices/1758686','60413/notices/1758691','60413/notices/1758685','60413/notices/1758699','60413/notices/1758694','60413/notices/1758701','60413/notices/1758684','60413/notices/1758688','60413/notices/1758683','60413/notices/1758695','60413/notices/1758696','60413/notices/1758687','60413/notices/1758680','60413/notices/1758692','60413/notices/1758700','60413/notices/1758679','60413/notices/1758682','60413/notices/1758681','60413/notices/1758690','60413/notices/1758689','60413/notices/1758693','60414/notices/1759591','60414/notices/1759604','60414/notices/1759593','60414/notices/1759599','60414/notices/1759595','60414/notices/1759590','60414/notices/1759592','60414/notices/1759603','60414/notices/1759598','60414/notices/1759602','60414/notices/1759596','60414/notices/1759597','60414/notices/1759600','60414/notices/1759594','60414/notices/1759601','60415/notices/1762161','60415/notices/1762172','60415/notices/1762171','60415/notices/1762163','60415/notices/1762168','60415/notices/1762155','60415/notices/1762178','60415/notices/1762167','60415/notices/1762153','60415/notices/1762151','60415/notices/1762176','60415/notices/1762154','60415/notices/1762173','60415/notices/1762152','60415/notices/1762175','60415/notices/1762174','60415/notices/1762170','60415/notices/1762164','60415/notices/1762156','60415/notices/1762160','60415/notices/1762166','60415/notices/1762169','60415/notices/1762157','60415/notices/1762162','60415/notices/1762165','60415/notices/1762159','60415/notices/1762158','60415/notices/1762177','60418/notices/1761760','60418/notices/1761739','60418/notices/1761768','60418/notices/1761745','60418/notices/1761755','60418/notices/1761743','60418/notices/1761749','60418/notices/1761751','60418/notices/1761757','60418/notices/1761758','60418/notices/1761742','60418/notices/1761762','60418/notices/1761761','60418/notices/1761748','60418/notices/1761741','60418/notices/1761754','60418/notices/1761750','60418/notices/1761747','60418/notices/1761740','60418/notices/1761767','60418/notices/1761746','60418/notices/1761763','60418/notices/1761764','60418/notices/1761756','60418/notices/1761759','60418/notices/1761765','60418/notices/1761766','60418/notices/1761753','60418/notices/1761752','60418/notices/1761744','60419/notices/1763079','60419/notices/1763069','60419/notices/1763067','60419/notices/1763073','60419/notices/1763071','60419/notices/1763074','60419/notices/1763080','60419/notices/1763077','60419/notices/1763070','60419/notices/1763064','60419/notices/1763078','60419/notices/1763072','60419/notices/1763066','60419/notices/1763076','60419/notices/1763065','60419/notices/1763075','60419/notices/1763081','60419/notices/1763068','60419/notices/1763063','60420/notices/1764173','60420/notices/1764171','60420/notices/1764176','60420/notices/1764175','60420/notices/1764170','60420/notices/1764169','60420/notices/1764172','60420/notices/1764174','60422/notices/1765295','60422/notices/1765294','60422/notices/1765297','60422/notices/1765296','60423/notices/1765723','60423/notices/1765730','60423/notices/1765734','60423/notices/1765727','60423/notices/1765731','60423/notices/1765728','60423/notices/1765724','60423/notices/1765733','60423/notices/1765726','60423/notices/1765729','60423/notices/1765732','60423/notices/1765725','60426/notices/1766657','60426/notices/1766653','60426/notices/1766652','60426/notices/1766656','60426/notices/1766651','60426/notices/1766655','60426/notices/1766650','60426/notices/1766654','60426/notices/1766658','60427/notices/1767505','60427/notices/1767507','60427/notices/1767493','60427/notices/1767499','60427/notices/1767492','60427/notices/1767506','60427/notices/1767500','60427/notices/1767497','60427/notices/1767498','60427/notices/1767504','60427/notices/1767503','60427/notices/1767494','60427/notices/1767495','60427/notices/1767496','60427/notices/1767502','60427/notices/1767501','60428/notices/1769203','60428/notices/1769180','60428/notices/1769189','60428/notices/1769198','60428/notices/1769183','60428/notices/1769199','60428/notices/1769182','60428/notices/1769185','60428/notices/1769196','60428/notices/1769188','60428/notices/1769181','60428/notices/1769178','60428/notices/1769190','60428/notices/1769195','60428/notices/1769186','60428/notices/1769194','60428/notices/1769192','60428/notices/1769193','60428/notices/1769179','60428/notices/1769184','60428/notices/1769202','60428/notices/1769191','60428/notices/1769197','60428/notices/1769187','60428/notices/1769177','60428/notices/1769200','60428/notices/1769201','60429/notices/1769594','60429/notices/1769590','60429/notices/1769593','60429/notices/1769592','60429/notices/1769595','60429/notices/1769591','60430/notices/1770600','60430/notices/1770590','60430/notices/1770597','60430/notices/1770598','60430/notices/1770594','60430/notices/1770599','60430/notices/1770596','60430/notices/1770589','60430/notices/1770593','60430/notices/1770592','60430/notices/1770595','60430/notices/1770591','60433/notices/1771449','60433/notices/1771456','60433/notices/1771459','60433/notices/1771454','60433/notices/1771453','60433/notices/1771452','60433/notices/1771455','60433/notices/1771450','60433/notices/1771457','60433/notices/1771451','60433/notices/1771460','60433/notices/1771458','60434/notices/1772190','60434/notices/1772201','60434/notices/1772200','60434/notices/1772187','60434/notices/1772195','60434/notices/1772192','60434/notices/1772189','60434/notices/1772191','60434/notices/1772185','60434/notices/1772199','60434/notices/1772193','60434/notices/1772196','60434/notices/1772194','60434/notices/1772188','60434/notices/1772186','60434/notices/1772198','60434/notices/1772197','60434/notices/1772184','60434/notices/1772183','60435/notices/1772973','60435/notices/1772967','60435/notices/1772969','60435/notices/1772965','60435/notices/1772968','60435/notices/1772977','60435/notices/1772972','60435/notices/1772976','60435/notices/1772964','60435/notices/1772963','60435/notices/1772975','60435/notices/1772978','60435/notices/1772971','60435/notices/1772974','60435/notices/1772970','60435/notices/1772966']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)


