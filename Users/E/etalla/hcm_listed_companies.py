# this scrapers retrieves the names, tickers and profile pages of all the companies listed on the Ho Chi Minh Stock Exchange.

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import mechanize 
import re

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

url = 'http://www.hsx.vn/hsx_en/Modules/Danhsach/Chungkhoan.aspx'


br = mechanize.Browser()
br.addheaders = [ ['User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'] ]
response = br.open(url)

br.select_form(name="aspnetForm")
br["ctl00$mainContent$Chungkhoan1_new$ddlLinhvuc"] = ["SIC       "]

response = br.submit()
code = safe_unicode(response.read())

root = lxml.html.document_fromstring(code)

def get_companies_list():
    root = lxml.html.document_fromstring(code)
    companies = (root.find("body")
                .findall("form")[0]
                .findall("table")[0].findall("tr")[0].findall("td")[0]
                .findall("table")[0].findall("tr")[0].findall("td")[0]
                .findall("table")[1].findall("tr")[0].findall("td")[1]
                .findall("table")[0].findall("tr")[0].findall("td")[1].findall("marquee")[0])
    company = {}
    position = 0 
    symbols = []

    for i in companies[0:len(companies):3]:
        company["symbol"] = i.text[:3]
        symbols.append(company["symbol"])
        company["link"] = 'http://www.hsx.vn/hsx_en/Modules/Danhsach/SymbolDetail.aspx?type=S&MCty='+company["symbol"]
        print company["link"]
        root = lxml.html.parse(company["link"]).getroot()
        retry = 0
        while not root and retry < 5:
            root = lxml.html.parse(company["link"]).getroot()
            retry += 1
        if root:
            name = (root.find("body")
            .findall("form")[0].findall("table")[0].findall("tr")[0].findall("td")[0].findall("table")[0].findall("tr")[2].findall("td")[0]
            .findall("table")[0].findall("tr")[0].findall("td")[2].findall("table")[0].findall("tr")[1].findall("td")[0]
            .findall("table")[0].findall("tr")[0].findall("td")[0].findall("div")[1].findall("div")[0].findall("table")[0]
            .findall("tr")[0].findall("td")[0].findall("div")[0].findall("table")[0])
            if len(name)!=0:
                name = name.findall("tr")[3].findall("td")[1]
                company["name"] = safe_unicode(name.text)
                scraperwiki.sqlite.save(['symbol','name','link'], company)
                position=position+1
            else:
                position=position+1

get_companies_list()

