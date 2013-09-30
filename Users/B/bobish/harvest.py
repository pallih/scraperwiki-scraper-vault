import scraperwiki
import urlparse
import lxml.html
import sys, time, os
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import urllib, urllib2
import urllib2, re

company_code = []

def open_url_with_proxy(url):

    proxy_list_url = "http://proxy-ip-list.com/free-usa-proxy-ip.html"
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    html = opener.open(proxy_list_url).read()
    soup = BeautifulSoup(html)
    data_table = soup.findAll("tr")
    proxies = []
    for row in data_table[1:]:
        table_cells = row.findAll("td")
        if table_cells and len(table_cells) > 0:    
            proxies.append(table_cells[0].text.strip())
        
    scraperwiki.sqlite.save_var("proxie_urls", ",".join(proxies))
    
    
    #url = "http://www.localharvest.org/store/candy.jsp"
    proxy = urllib2.ProxyHandler({'http': proxies[0]})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    x = urllib2.urlopen(url).read()
    
    return x



counter = 0
#company = []
def read_detail_page(each_company_url):

    def clean(text):
        text = text.replace("u\'","")
        text = text.replace("\'","")
        text = text.replace("\\xa0","")
        text = text.strip('[]')
        return text
    global counter
    counter = counter + 1
    html = scraperwiki.scrape(each_company_url)
    tree = lxml.html.parse(each_company_url)
    
    data = {}
    
    data['id'] = counter
    data['companyname'] = tree.xpath("//table[@id='company']/tr[1]/td/text()")
    data['companyname'] = clean(str(data['companyname']))
    data['address'] = tree.xpath("//table[@id='company']/tr[2]/td/text()")
    data['address'] = clean(str(data['address']))
    data['zip'] = tree.xpath("//table[@id='company']/tr[3]/td/text()")
    data['zip'] = clean(str(data['zip']))
    data['city'] = tree.xpath("//table[@id='company']/tr[4]/td/text()")
    data['city'] = clean(str(data['city']))
    data['country'] = tree.xpath("//table[@id='company']/tr[6]/td/text()")
    data['country'] = clean(str(data['country']))
    data['phonenumber'] = tree.xpath("//table[@id='company']/tr[7]/td/text()")
    data['phonenumber'] = clean(str(data['phonenumber']))
    data['faxnumber'] = tree.xpath("//table[@id='company']/tr[8]/td/text()")
    data['faxnumber'] = clean(str(data['faxnumber']))
    data['emails'] = tree.xpath("//table[@id='company']/tr[9]/td/a/text()")
    data['emails'] = clean(str(data['emails']))
    data['website'] = tree.xpath("//table[@id='company']/tr[10]/td/a/text()")
    data['website'] = clean(str(data['website']))
    data['salesmethod'] = tree.xpath("//table[@id='company']/tr[11]/td/text()")
    data['salesmethod'] = clean(str(data['salesmethod']))
    data['certifications'] = tree.xpath("//table[@id='company']/tr[12]/td/text()")
    data['certifications'] = clean(str(data['certifications']))
    data['yearfounded'] = tree.xpath("//table[@id='company']/tr[17]/td/text()")
    data['yearfounded'] = clean(str(data['yearfounded']))
    contactname = tree.xpath("//table[@id='company']/tr[18]/td/text()")
    contactname = clean(str(contactname))
    
    if contactname:
        contactname = str(contactname)
        no_words = len(contactname.split(" ",))
        wordindex = no_words-1
        title = contactname.split(" ",no_words)[0]
        
        if wordindex == 2:
            data['contact1first'] = contactname.split(" ",no_words)[1]
            data['contact1last'] = contactname.split(" ",no_words)[2]
            contactname.split(" ",no_words)[0]
            if title in ('Mr.','Mrs','Ms','Mrs.'):
                data['contact1title'] = contactname.split(" ",no_words)[0]
        if wordindex == 1:
            data['contact1first'] = contactname.split(" ",no_words)[0]
            data['contact1last'] = contactname.split(" ",no_words)[1]
        if wordindex > 2:
            data['contact1first'] = contactname.split(" ",no_words)[1]
            data['contact1last'] = contactname.split(" ",no_words)[1].join(" ").join(contactname.split(" ",no_words)[2:])
            if title in ('Mr.','Mrs','Ms','Mrs.'):
                data['contact1title'] = contactname.split(" ",no_words)[0]

    data['categories'] = tree.xpath("//table[@id='company']/tr[21]/td/text()")
    data['categories'] = clean(str(data['categories']))
    data['description'] = tree.xpath("//table[@id='company']/tr[23]/td/text()")
    data['description'] = clean(str(data['description']))
    data['sourceurl'] = each_company_url
    scraperwiki.sqlite.save(['id'], data)

def read_company_links(suburl):
    

    root = open_url_with_proxy(suburl)
    root = lxml.html.fromstring(root)

    for el in root.cssselect("font.txt0 a"):
        if el.attrib['href'].find("/M") != -1:
            code = el.attrib['href']
            global company_code
            if code not in company_code:
                company_code.append(code)
    
    for c in range(0,len(company_code)):
        print company_code[c]



def read_all_result_page_links_for(mainurl):

    root = open_url_with_proxy(mainurl)
    root = lxml.html.fromstring(root)

    print root
    for el in root.cssselect("p.txt0 a"):
        print "Reached"
        gen_url = "https://www.localharvest.org"+ el.attrib['href']
        read_company_links(gen_url)

def scrape_harvest():
    scraperwiki.sqlite.attach("proxy_test", "src")
    #print scraperwiki.sqlite.get_var("proxy_csv").split(",") # array of proxies to use


# how to use the proxies with urllib2
#url = "http://www.localharvest.org/store/"

    harvest_url= "https://www.localharvest.org/store/candy.jsp"
    proxy = urllib2.ProxyHandler({'http': '98.200.244.40', 'port': '1537'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    x = urllib2.urlopen(harvest_url).read()


    html = scraperwiki.scrape(x)
    tree = lxml.html.parse(x)
    print tree

    #pagelist = tree.xpath(".//*[@id='pages']/a[12]/text()")
    #lastpage = int(pagelist[0])
    #page_count = lastpage+1

    #for page in range(1,page_count):
    #read_all_result_page_links_for(url)
    #open_url_with_proxy(url)

scrape_harvest()

import scraperwiki
import urlparse
import lxml.html
import sys, time, os
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import urllib, urllib2
import urllib2, re

company_code = []

def open_url_with_proxy(url):

    proxy_list_url = "http://proxy-ip-list.com/free-usa-proxy-ip.html"
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    html = opener.open(proxy_list_url).read()
    soup = BeautifulSoup(html)
    data_table = soup.findAll("tr")
    proxies = []
    for row in data_table[1:]:
        table_cells = row.findAll("td")
        if table_cells and len(table_cells) > 0:    
            proxies.append(table_cells[0].text.strip())
        
    scraperwiki.sqlite.save_var("proxie_urls", ",".join(proxies))
    
    
    #url = "http://www.localharvest.org/store/candy.jsp"
    proxy = urllib2.ProxyHandler({'http': proxies[0]})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    x = urllib2.urlopen(url).read()
    
    return x



counter = 0
#company = []
def read_detail_page(each_company_url):

    def clean(text):
        text = text.replace("u\'","")
        text = text.replace("\'","")
        text = text.replace("\\xa0","")
        text = text.strip('[]')
        return text
    global counter
    counter = counter + 1
    html = scraperwiki.scrape(each_company_url)
    tree = lxml.html.parse(each_company_url)
    
    data = {}
    
    data['id'] = counter
    data['companyname'] = tree.xpath("//table[@id='company']/tr[1]/td/text()")
    data['companyname'] = clean(str(data['companyname']))
    data['address'] = tree.xpath("//table[@id='company']/tr[2]/td/text()")
    data['address'] = clean(str(data['address']))
    data['zip'] = tree.xpath("//table[@id='company']/tr[3]/td/text()")
    data['zip'] = clean(str(data['zip']))
    data['city'] = tree.xpath("//table[@id='company']/tr[4]/td/text()")
    data['city'] = clean(str(data['city']))
    data['country'] = tree.xpath("//table[@id='company']/tr[6]/td/text()")
    data['country'] = clean(str(data['country']))
    data['phonenumber'] = tree.xpath("//table[@id='company']/tr[7]/td/text()")
    data['phonenumber'] = clean(str(data['phonenumber']))
    data['faxnumber'] = tree.xpath("//table[@id='company']/tr[8]/td/text()")
    data['faxnumber'] = clean(str(data['faxnumber']))
    data['emails'] = tree.xpath("//table[@id='company']/tr[9]/td/a/text()")
    data['emails'] = clean(str(data['emails']))
    data['website'] = tree.xpath("//table[@id='company']/tr[10]/td/a/text()")
    data['website'] = clean(str(data['website']))
    data['salesmethod'] = tree.xpath("//table[@id='company']/tr[11]/td/text()")
    data['salesmethod'] = clean(str(data['salesmethod']))
    data['certifications'] = tree.xpath("//table[@id='company']/tr[12]/td/text()")
    data['certifications'] = clean(str(data['certifications']))
    data['yearfounded'] = tree.xpath("//table[@id='company']/tr[17]/td/text()")
    data['yearfounded'] = clean(str(data['yearfounded']))
    contactname = tree.xpath("//table[@id='company']/tr[18]/td/text()")
    contactname = clean(str(contactname))
    
    if contactname:
        contactname = str(contactname)
        no_words = len(contactname.split(" ",))
        wordindex = no_words-1
        title = contactname.split(" ",no_words)[0]
        
        if wordindex == 2:
            data['contact1first'] = contactname.split(" ",no_words)[1]
            data['contact1last'] = contactname.split(" ",no_words)[2]
            contactname.split(" ",no_words)[0]
            if title in ('Mr.','Mrs','Ms','Mrs.'):
                data['contact1title'] = contactname.split(" ",no_words)[0]
        if wordindex == 1:
            data['contact1first'] = contactname.split(" ",no_words)[0]
            data['contact1last'] = contactname.split(" ",no_words)[1]
        if wordindex > 2:
            data['contact1first'] = contactname.split(" ",no_words)[1]
            data['contact1last'] = contactname.split(" ",no_words)[1].join(" ").join(contactname.split(" ",no_words)[2:])
            if title in ('Mr.','Mrs','Ms','Mrs.'):
                data['contact1title'] = contactname.split(" ",no_words)[0]

    data['categories'] = tree.xpath("//table[@id='company']/tr[21]/td/text()")
    data['categories'] = clean(str(data['categories']))
    data['description'] = tree.xpath("//table[@id='company']/tr[23]/td/text()")
    data['description'] = clean(str(data['description']))
    data['sourceurl'] = each_company_url
    scraperwiki.sqlite.save(['id'], data)

def read_company_links(suburl):
    

    root = open_url_with_proxy(suburl)
    root = lxml.html.fromstring(root)

    for el in root.cssselect("font.txt0 a"):
        if el.attrib['href'].find("/M") != -1:
            code = el.attrib['href']
            global company_code
            if code not in company_code:
                company_code.append(code)
    
    for c in range(0,len(company_code)):
        print company_code[c]



def read_all_result_page_links_for(mainurl):

    root = open_url_with_proxy(mainurl)
    root = lxml.html.fromstring(root)

    print root
    for el in root.cssselect("p.txt0 a"):
        print "Reached"
        gen_url = "https://www.localharvest.org"+ el.attrib['href']
        read_company_links(gen_url)

def scrape_harvest():
    scraperwiki.sqlite.attach("proxy_test", "src")
    #print scraperwiki.sqlite.get_var("proxy_csv").split(",") # array of proxies to use


# how to use the proxies with urllib2
#url = "http://www.localharvest.org/store/"

    harvest_url= "https://www.localharvest.org/store/candy.jsp"
    proxy = urllib2.ProxyHandler({'http': '98.200.244.40', 'port': '1537'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    x = urllib2.urlopen(harvest_url).read()


    html = scraperwiki.scrape(x)
    tree = lxml.html.parse(x)
    print tree

    #pagelist = tree.xpath(".//*[@id='pages']/a[12]/text()")
    #lastpage = int(pagelist[0])
    #page_count = lastpage+1

    #for page in range(1,page_count):
    #read_all_result_page_links_for(url)
    #open_url_with_proxy(url)

scrape_harvest()

