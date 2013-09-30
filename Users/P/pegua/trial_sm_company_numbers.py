import scraperwiki
import lxml.html
import datetime

SITE = "https://registroimprese.cc.sm/"
SEARCH_SITE = SITE + "ricerca.asp?imp_coe="

#how many company number are controlled for each run
#after the last valid company found
EMPTY_BEFORE_EXIT = 50


def get_company_info(company_number):
    '''
    Get company info for a given company number.
    Returning a dict with the information, with 
    CompanyNumber set to -1 if no company is found.
    '''
    html = scraperwiki.scrape(SEARCH_SITE+str(company_number))
    if( html.find("The search did not produce any results") != -1 ):
        info = {"CompanyNumber":-1}
    else:
        root = lxml.html.fromstring(html)
        info = {}
        info["CompanyNumber"] = company_number
        tables = root.cssselect("table")
        table = tables[7]
        tds = table.cssselect("td")
        td = tds[1]
        fonts = td.cssselect("font")
        info["CompanyName"] = fonts[0].text
        brs = td.cssselect("br")
        info["Address"] = lxml.html.tostring(brs[1]).replace("<br>&#13;","")
        zip_city = lxml.html.tostring(brs[2]).replace("<br>&#13;","")
        info["PostalCode"] = zip_city.split('-')[0].strip(" ")
        info["City"] = zip_city.split('-')[1].strip(" ")
        info["ScrapedTime"] = datetime.datetime.now()
        status_code = fonts[1].text.split(":")
        info["Status"] = status_code[0]
        if( len(status_code) == 2 ):
            info["LicenceCode"] = status_code[1].strip()
        

    return info

#get the last saved company 
max_coe = scraperwiki.sqlite.select("max(CompanyNumber) as max_code from swdata")
last_page = max_coe[0]["max_code"]


for i in range(last_page,100000):
    info = get_company_info(i)
    if( info["CompanyNumber"] != -1 ):
        scraperwiki.sqlite.save(["CompanyNumber"],info)
        last_page = i

    if( i  == last_page+EMPTY_BEFORE_EXIT ):
        break


import scraperwiki
import lxml.html
import datetime

SITE = "https://registroimprese.cc.sm/"
SEARCH_SITE = SITE + "ricerca.asp?imp_coe="

#how many company number are controlled for each run
#after the last valid company found
EMPTY_BEFORE_EXIT = 50


def get_company_info(company_number):
    '''
    Get company info for a given company number.
    Returning a dict with the information, with 
    CompanyNumber set to -1 if no company is found.
    '''
    html = scraperwiki.scrape(SEARCH_SITE+str(company_number))
    if( html.find("The search did not produce any results") != -1 ):
        info = {"CompanyNumber":-1}
    else:
        root = lxml.html.fromstring(html)
        info = {}
        info["CompanyNumber"] = company_number
        tables = root.cssselect("table")
        table = tables[7]
        tds = table.cssselect("td")
        td = tds[1]
        fonts = td.cssselect("font")
        info["CompanyName"] = fonts[0].text
        brs = td.cssselect("br")
        info["Address"] = lxml.html.tostring(brs[1]).replace("<br>&#13;","")
        zip_city = lxml.html.tostring(brs[2]).replace("<br>&#13;","")
        info["PostalCode"] = zip_city.split('-')[0].strip(" ")
        info["City"] = zip_city.split('-')[1].strip(" ")
        info["ScrapedTime"] = datetime.datetime.now()
        status_code = fonts[1].text.split(":")
        info["Status"] = status_code[0]
        if( len(status_code) == 2 ):
            info["LicenceCode"] = status_code[1].strip()
        

    return info

#get the last saved company 
max_coe = scraperwiki.sqlite.select("max(CompanyNumber) as max_code from swdata")
last_page = max_coe[0]["max_code"]


for i in range(last_page,100000):
    info = get_company_info(i)
    if( info["CompanyNumber"] != -1 ):
        scraperwiki.sqlite.save(["CompanyNumber"],info)
        last_page = i

    if( i  == last_page+EMPTY_BEFORE_EXIT ):
        break


