import scraperwiki
import urlparse
import lxml.html
import sys, time, os
from mechanize import Browser

def read_detail_page(each_company_url,companycount):

    def clean(text):
        text = text.replace("u\'","")
        text = text.replace("\'","")
        text = text.replace("\\xa0","")
        text = text.strip('[]')
        return text
        
    
    #scraperwiki.sqlite.attach("url_data", "src")
    
    #results = scraperwiki.sqlite.select("url from src.swdata limit 909")
    
    #for company in results:
    #companyurl = company['url']
    #url = "{0}".format(companyurl)
    html = scraperwiki.scrape(each_company_url)
    
    tree = lxml.html.parse(each_company_url)
    
    data = {}
    
    data['id'] = companycount
    data['companyname'] = tree.xpath("//table[@id='company']/tr[1]/td/text()")
    data['companyname'] = clean(str(data['companyname']))
    data['address'] = tree.xpath("//table[@id='company']/tr[2]/td/text()")
    data['address'] = clean(str(data['address']))
    data['zip'] = tree.xpath("//table[@id='company']/tr[3]/td/text()")
    data['zip'] = clean(str(data['zip']))
    data['city'] = tree.xpath("//table[@id='company']/tr[4]/td/text()")
    data['city'] = clean(str(data['city']))
    #data['region'] = tree.xpath("//table[@id='company']/tr[5]/td/text()")
    #data['region'] = clean(str(data['region']))
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
    #data['company_certificate'] = tree.xpath("//table[@id='company']/tr[13]/td/text()")
    #data['company_certificate'] = clean(str(data['company_certificate']))
    #data['link_tocertificate'] = tree.xpath("//table[@id='company']/tr[14]/td/text()")
    #data['link_tocertificate'] = clean(str(data['link_tocertificate']))
    #data['label'] = tree.xpath("//table[@id='company']/tr[15]/td/text()")
    #data['label'] = clean(str(data['label']))
    #data['surface'] = tree.xpath("//table[@id='company']/tr[16]/td/text()")
    #data['surface'] = clean(str(data['surface']))
    data['yearfounded'] = tree.xpath("//table[@id='company']/tr[17]/td/text()")
    data['yearfounded'] = clean(str(data['yearfounded']))
    contactname = tree.xpath("//table[@id='company']/tr[18]/td/text()")
    contactname = clean(str(contactname))
    print contactname
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
            #arr[1].join(" ").join(arr[2:])
            data['contact1last'] = contactname.split(" ",no_words)[1].join(" ").join(contactname.split(" ",no_words)[2:])
            if title in ('Mr.','Mrs','Ms','Mrs.'):
                data['contact1title'] = contactname.split(" ",no_words)[0]

              
    #data['product_sell'] = tree.xpath("//table[@id='company']/tr[19]/td/text()")
    #data['product_sell'] = clean(str(data['product_sell']))
    #data['product_buy'] = tree.xpath("//table[@id='company']/tr[20]/td/text()")
    #data['product_buy'] = clean(str(data['product_buy']))
    data['categories'] = tree.xpath("//table[@id='company']/tr[21]/td/text()")
    data['categories'] = clean(str(data['categories']))
    data['description'] = tree.xpath("//table[@id='company']/tr[23]/td/text()")
    data['description'] = clean(str(data['description']))
    data['sourceurl'] = each_company_url
    scraperwiki.sqlite.save(['id'], data)

def read_all_result_page_links_for(mainurl):
    br = Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i = 0
    global_list =[]
    
    br.open(mainurl)
    nice_links = [l for l in br.links()
            if 'company' in l.url]
        
        #global_list.extend(nice_links)
    
        #record = {}
    for link in nice_links:
    
        i=i+1
        read_detail_page(link.url,i)
        #print link.url
        #scraperwiki.sqlite.save(["id"], record)

def getResultPages():
    global counter
    counter = 0
    organic_url= "http://www.organic-bio.com/en/advanced-search2/?country=174&prgrp2=0&prodgrp2=0&prgrp3=0&prodgrp3=0&name=&city=&contact=&certification=0&service=0&fair=0"
    html = scraperwiki.scrape(organic_url)
    tree = lxml.html.parse(organic_url)
    pagelist = tree.xpath(".//*[@id='pages']/a[12]/text()")
    lastpage = int(pagelist[0])
    page_count = lastpage+1

    #page_count = get_page_count()
    for page in range(1,page_count):
        url = "http://www.organic-bio.com/en/advanced-search2/?page={0}&country=174&prgrp2=0&prodgrp2=0&prgrp3=0&prodgrp3=0&name=&city=&contact=&certification=0&service=0&fair=0".format(page)
        read_all_result_page_links_for(url)

getResultPages()
import scraperwiki
import urlparse
import lxml.html
import sys, time, os
from mechanize import Browser

def read_detail_page(each_company_url,companycount):

    def clean(text):
        text = text.replace("u\'","")
        text = text.replace("\'","")
        text = text.replace("\\xa0","")
        text = text.strip('[]')
        return text
        
    
    #scraperwiki.sqlite.attach("url_data", "src")
    
    #results = scraperwiki.sqlite.select("url from src.swdata limit 909")
    
    #for company in results:
    #companyurl = company['url']
    #url = "{0}".format(companyurl)
    html = scraperwiki.scrape(each_company_url)
    
    tree = lxml.html.parse(each_company_url)
    
    data = {}
    
    data['id'] = companycount
    data['companyname'] = tree.xpath("//table[@id='company']/tr[1]/td/text()")
    data['companyname'] = clean(str(data['companyname']))
    data['address'] = tree.xpath("//table[@id='company']/tr[2]/td/text()")
    data['address'] = clean(str(data['address']))
    data['zip'] = tree.xpath("//table[@id='company']/tr[3]/td/text()")
    data['zip'] = clean(str(data['zip']))
    data['city'] = tree.xpath("//table[@id='company']/tr[4]/td/text()")
    data['city'] = clean(str(data['city']))
    #data['region'] = tree.xpath("//table[@id='company']/tr[5]/td/text()")
    #data['region'] = clean(str(data['region']))
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
    #data['company_certificate'] = tree.xpath("//table[@id='company']/tr[13]/td/text()")
    #data['company_certificate'] = clean(str(data['company_certificate']))
    #data['link_tocertificate'] = tree.xpath("//table[@id='company']/tr[14]/td/text()")
    #data['link_tocertificate'] = clean(str(data['link_tocertificate']))
    #data['label'] = tree.xpath("//table[@id='company']/tr[15]/td/text()")
    #data['label'] = clean(str(data['label']))
    #data['surface'] = tree.xpath("//table[@id='company']/tr[16]/td/text()")
    #data['surface'] = clean(str(data['surface']))
    data['yearfounded'] = tree.xpath("//table[@id='company']/tr[17]/td/text()")
    data['yearfounded'] = clean(str(data['yearfounded']))
    contactname = tree.xpath("//table[@id='company']/tr[18]/td/text()")
    contactname = clean(str(contactname))
    print contactname
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
            #arr[1].join(" ").join(arr[2:])
            data['contact1last'] = contactname.split(" ",no_words)[1].join(" ").join(contactname.split(" ",no_words)[2:])
            if title in ('Mr.','Mrs','Ms','Mrs.'):
                data['contact1title'] = contactname.split(" ",no_words)[0]

              
    #data['product_sell'] = tree.xpath("//table[@id='company']/tr[19]/td/text()")
    #data['product_sell'] = clean(str(data['product_sell']))
    #data['product_buy'] = tree.xpath("//table[@id='company']/tr[20]/td/text()")
    #data['product_buy'] = clean(str(data['product_buy']))
    data['categories'] = tree.xpath("//table[@id='company']/tr[21]/td/text()")
    data['categories'] = clean(str(data['categories']))
    data['description'] = tree.xpath("//table[@id='company']/tr[23]/td/text()")
    data['description'] = clean(str(data['description']))
    data['sourceurl'] = each_company_url
    scraperwiki.sqlite.save(['id'], data)

def read_all_result_page_links_for(mainurl):
    br = Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i = 0
    global_list =[]
    
    br.open(mainurl)
    nice_links = [l for l in br.links()
            if 'company' in l.url]
        
        #global_list.extend(nice_links)
    
        #record = {}
    for link in nice_links:
    
        i=i+1
        read_detail_page(link.url,i)
        #print link.url
        #scraperwiki.sqlite.save(["id"], record)

def getResultPages():
    global counter
    counter = 0
    organic_url= "http://www.organic-bio.com/en/advanced-search2/?country=174&prgrp2=0&prodgrp2=0&prgrp3=0&prodgrp3=0&name=&city=&contact=&certification=0&service=0&fair=0"
    html = scraperwiki.scrape(organic_url)
    tree = lxml.html.parse(organic_url)
    pagelist = tree.xpath(".//*[@id='pages']/a[12]/text()")
    lastpage = int(pagelist[0])
    page_count = lastpage+1

    #page_count = get_page_count()
    for page in range(1,page_count):
        url = "http://www.organic-bio.com/en/advanced-search2/?page={0}&country=174&prgrp2=0&prodgrp2=0&prgrp3=0&prodgrp3=0&name=&city=&contact=&certification=0&service=0&fair=0".format(page)
        read_all_result_page_links_for(url)

getResultPages()
