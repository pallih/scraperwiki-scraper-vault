import scraperwiki

# Blank Python

import re
import mechanize 
from BeautifulSoup import BeautifulSoup

br=mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def myscrapper(url):    
    response = br.open(url)
    html = response.read()
    soup = BeautifulSoup(html)
    scrapped = {}
    nextPage = soup.find("a", {"id":"next_page"})
    print nextPage
    if nextPage:
        url =  nextPage["href"]
    else:
        url = None
    companies = soup.findAll("div", {"class":"item_resultat_mea"})
    for company in companies:
        com = {}
        title = company.find("a", id=re.compile("^linkComp\d+"))
        if title:
            com["name"]=title["title"]
            com["url"]= title["href"]
        
        country = company.find("span", id=re.compile("^country\d+"))
        if country :
            com["country"]=country.text
    
        city = company.find("span", id=re.compile("^city\d+"))
        if city:
            com["city"]=city.text
    
        postal = company.find("span", id=re.compile("^postalCode\d+"))
        if postal:
            com["postal"]=postal.text
    
        phone = company.find("span", id=re.compile("^phoneNumberId\d*"))
        if phone:
            com["phone"]=phone.text
    
        fax = company.find("span", id=re.compile("^faxNumberId\d+"))
        print fax
        if fax:
            com["fax"] = fax.text
    
        scraperwiki.sqlite.save(["name"],com)


#    if url:
#        myscrapper(url)
        



url = "http://in.kompass.com/MarketingViewWeb/appmanager/kim/IND_Portal?_nfpb=true&_windowLabel=searchPdtSvces_1_1&searchPdtSvces_1_1_actionOverride=%2Fflows%2FmarketingInformation%2FsearchPdtSvces%2FdisplayList&searchPdtSvces_1_1searchExp=Graphic+design+services&searchPdtSvces_1_1geoSearch=MKT_GEO2&searchPdtSvces_1_1geoUnitGeoScopeRegion=&searchPdtSvces_1_1geoDistributionCode=MKT_GEO2&searchPdtSvces_1_1geoUnitGeoScopeCountry=CHL%2CMEX%2CUSA%2CCAN%2CBRA&searchPdtSvces_1_1geoUnitGeoScopeDistrict=&searchPdtSvces_1_1CodeLevel=7&searchPdtSvces_1_1geoCode=internationalEntity.MKT_GEO2&searchPdtSvces_1_1typeOfGeoDistribution=MKT_GEO&searchPdtSvces_1_1CodeId=8141010&_pageLabel=marketingInformation_productServicesPage#.UaYGk-vUQ1L"

myscrapper(url)
import scraperwiki

# Blank Python

import re
import mechanize 
from BeautifulSoup import BeautifulSoup

br=mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def myscrapper(url):    
    response = br.open(url)
    html = response.read()
    soup = BeautifulSoup(html)
    scrapped = {}
    nextPage = soup.find("a", {"id":"next_page"})
    print nextPage
    if nextPage:
        url =  nextPage["href"]
    else:
        url = None
    companies = soup.findAll("div", {"class":"item_resultat_mea"})
    for company in companies:
        com = {}
        title = company.find("a", id=re.compile("^linkComp\d+"))
        if title:
            com["name"]=title["title"]
            com["url"]= title["href"]
        
        country = company.find("span", id=re.compile("^country\d+"))
        if country :
            com["country"]=country.text
    
        city = company.find("span", id=re.compile("^city\d+"))
        if city:
            com["city"]=city.text
    
        postal = company.find("span", id=re.compile("^postalCode\d+"))
        if postal:
            com["postal"]=postal.text
    
        phone = company.find("span", id=re.compile("^phoneNumberId\d*"))
        if phone:
            com["phone"]=phone.text
    
        fax = company.find("span", id=re.compile("^faxNumberId\d+"))
        print fax
        if fax:
            com["fax"] = fax.text
    
        scraperwiki.sqlite.save(["name"],com)


#    if url:
#        myscrapper(url)
        



url = "http://in.kompass.com/MarketingViewWeb/appmanager/kim/IND_Portal?_nfpb=true&_windowLabel=searchPdtSvces_1_1&searchPdtSvces_1_1_actionOverride=%2Fflows%2FmarketingInformation%2FsearchPdtSvces%2FdisplayList&searchPdtSvces_1_1searchExp=Graphic+design+services&searchPdtSvces_1_1geoSearch=MKT_GEO2&searchPdtSvces_1_1geoUnitGeoScopeRegion=&searchPdtSvces_1_1geoDistributionCode=MKT_GEO2&searchPdtSvces_1_1geoUnitGeoScopeCountry=CHL%2CMEX%2CUSA%2CCAN%2CBRA&searchPdtSvces_1_1geoUnitGeoScopeDistrict=&searchPdtSvces_1_1CodeLevel=7&searchPdtSvces_1_1geoCode=internationalEntity.MKT_GEO2&searchPdtSvces_1_1typeOfGeoDistribution=MKT_GEO&searchPdtSvces_1_1CodeId=8141010&_pageLabel=marketingInformation_productServicesPage#.UaYGk-vUQ1L"

myscrapper(url)
