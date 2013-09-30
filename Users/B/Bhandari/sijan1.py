import scraperwiki

# Blank Python
import scraperwiki
#import json #for json decoding
from lxml import etree     
from cStringIO import StringIO
import urllib

#import re


strAddr = "https://dl.dropboxusercontent.com/s/1w7eynfvb28g0p2/bhandariIdea.html?token_hash=AAHy5GCwaoZk78VlHPEBJUZAILnyHrOfSO-4ADAnVkVV1w&dl=1"
html = urllib.urlopen(strAddr)
html = html.read()
print html
parser = etree.HTMLParser()
tree   = etree.parse(StringIO(html), parser)
mainContent = tree.xpath("//table[@id='PeopleList']")[0]

#print mainContent

contentHTML= (etree.tostring(mainContent, pretty_print=True))

#print contentHTML
tree   = etree.parse(StringIO(contentHTML), parser)
lawyers = tree.xpath("//tbody/tr")
#print eachLawyer


TotalList = []
for eachLawyer in lawyers:
    print eachLawyer
    Total = {}

    contentHTML= (etree.tostring(eachLawyer, pretty_print=True))
    tree   = etree.parse(StringIO(contentHTML), parser)
    #print contentHTML
    Total['name'] = tree.xpath("//td/a/text()")[0].strip()
    print Total['name']    
    Total['link'] = tree.xpath("//td/a/@href")[0].strip()
    Total['title'] = tree.xpath("//td[2]/text()")[0].strip()
    email = tree.xpath("//td[3]/a/text()")
    if email!=[]:
        Total['email']=email[0].strip()
    else:
        Total['email']=""

    Total['location'] = tree.xpath("//td[4]/table/tr/td[1]/a/text()")[0].strip()
    Total['telephone'] = tree.xpath("//td[4]/table/tr/td[2]/text()")[0].strip()
    
    #print Total
    TotalList.append(Total)

print TotalList
    
i = 0
for total in TotalList:
    url = "http://www.lw.com" +total['link']
    #print url
    html = urllib.urlopen(url)
    html = html.read()

    #print html
    educationList = []
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(html), parser)
    mainContent = tree.xpath("//ul[@id='AttorneyMetaData']/li/ul[2]/descendant-or-self::*/text()")
    for eachEdu in mainContent:
        eachEdu = eachEdu.strip()
        #print eachEdu
        educationList.append(eachEdu)
    total["i"]=str(i)       
    total['education'] =  ':'.join(educationList)
    print total
    scraperwiki.sqlite.save(unique_keys=["i"], data=total)
    i=i+1



    
    

'''

productLinks=tree.xpath("//div[@class='sitemap-info']/div[@class='left']/ul/li/a/@href")

for link in productLinks:
    productLinks[productLinks.index(link)] = link+"&limit=1000000"

for link in productLinks:
    html = urllib.urlopen(link)
    html = html.read()
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html),parser)
    productGrids = tree.xpath("//div[@class='name']/parent::*")
    for product in productGrids:
        productHTML= (etree.tostring(product, pretty_print=True))
        tree = etree.parse(StringIO(productHTML),parser)
        image = tree.xpath("//div[@class='image']/a/img/@src")
        productLink= tree.xpath("//div[@class='name']/a/@href")
        name = tree.xpath("//div[@class='name']//text()")
        price = ''.join(tree.xpath("//span[@class='price-tax']/text()"))
        price=''.join(re.findall("([0-9]+,?[0-9]*\.?[0-9]*)*",price)).replace(',','')        
        description = tree.xpath("//div[@class='description']//text()")
        scraperwiki.sqlite.save(unique_keys=['productLink'], data={'productLink':''.join(productLink),'productName':''.join(name), 'price':''.join(price), 'description':''.join(description),'image':''.join(image)})

        
'''
'''
search = "site:yeskantipur.com"

for myI in range(10):
    startVal = myI*10+1
    strAddr = "https://www.googleapis.com/customsearch/v1?key=AIzaSyAu0Qjk8EhHfIZwZ5zRxeCYvRIt3M1DsjE&cx=013954637796931996224:b03wibgo-gq&start="+str(startVal)+"&q="+search
   
    html = urllib.urlopen(strAddr)
    Json = html.read()
    print Json
    output = json.loads(Json)
    message =""
    items = output['items']  or [] 
    for item in items:
        givenLink = item['link']
        #givenLink ="http://www.yeskantipur.com/index.php?route=product/product&product_id=3257"
    
        #html=scraperwiki.scrape(givenLink)
        html = urllib.urlopen(givenLink)
        html = html.read()
    
        parser = etree.HTMLParser()
        tree   = etree.parse(StringIO(html), parser)
    
        productNames=tree.xpath("//div[@class='product_title']/h1/text()")
        productName=""
        for pName in productNames:
            productName= pName
        prices= tree.xpath("//div[@class='price']/text()")
        price =""
        for prc in prices:
            price = prc
            price = price.replace("Price: ","").lstrip()
    
        if price=='':
            prices=tree.xpath("//div[@class='price']/span[@class='price-new']/text()")
            for prc in prices:
                price = prc
                price = price.replace("Price: ","").lstrip()
        
        description = tree.xpath("//div[@id='tab-description']//text()")
        message += productName + price
        for desc in description:
            desc+= " "+desc
        scraperwiki.sqlite.save(unique_keys=['link'], data={'link':givenLink,'productName':productName, 'price':price, 'description':description})

'''
import scraperwiki

# Blank Python
import scraperwiki
#import json #for json decoding
from lxml import etree     
from cStringIO import StringIO
import urllib

#import re


strAddr = "https://dl.dropboxusercontent.com/s/1w7eynfvb28g0p2/bhandariIdea.html?token_hash=AAHy5GCwaoZk78VlHPEBJUZAILnyHrOfSO-4ADAnVkVV1w&dl=1"
html = urllib.urlopen(strAddr)
html = html.read()
print html
parser = etree.HTMLParser()
tree   = etree.parse(StringIO(html), parser)
mainContent = tree.xpath("//table[@id='PeopleList']")[0]

#print mainContent

contentHTML= (etree.tostring(mainContent, pretty_print=True))

#print contentHTML
tree   = etree.parse(StringIO(contentHTML), parser)
lawyers = tree.xpath("//tbody/tr")
#print eachLawyer


TotalList = []
for eachLawyer in lawyers:
    print eachLawyer
    Total = {}

    contentHTML= (etree.tostring(eachLawyer, pretty_print=True))
    tree   = etree.parse(StringIO(contentHTML), parser)
    #print contentHTML
    Total['name'] = tree.xpath("//td/a/text()")[0].strip()
    print Total['name']    
    Total['link'] = tree.xpath("//td/a/@href")[0].strip()
    Total['title'] = tree.xpath("//td[2]/text()")[0].strip()
    email = tree.xpath("//td[3]/a/text()")
    if email!=[]:
        Total['email']=email[0].strip()
    else:
        Total['email']=""

    Total['location'] = tree.xpath("//td[4]/table/tr/td[1]/a/text()")[0].strip()
    Total['telephone'] = tree.xpath("//td[4]/table/tr/td[2]/text()")[0].strip()
    
    #print Total
    TotalList.append(Total)

print TotalList
    
i = 0
for total in TotalList:
    url = "http://www.lw.com" +total['link']
    #print url
    html = urllib.urlopen(url)
    html = html.read()

    #print html
    educationList = []
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(html), parser)
    mainContent = tree.xpath("//ul[@id='AttorneyMetaData']/li/ul[2]/descendant-or-self::*/text()")
    for eachEdu in mainContent:
        eachEdu = eachEdu.strip()
        #print eachEdu
        educationList.append(eachEdu)
    total["i"]=str(i)       
    total['education'] =  ':'.join(educationList)
    print total
    scraperwiki.sqlite.save(unique_keys=["i"], data=total)
    i=i+1



    
    

'''

productLinks=tree.xpath("//div[@class='sitemap-info']/div[@class='left']/ul/li/a/@href")

for link in productLinks:
    productLinks[productLinks.index(link)] = link+"&limit=1000000"

for link in productLinks:
    html = urllib.urlopen(link)
    html = html.read()
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html),parser)
    productGrids = tree.xpath("//div[@class='name']/parent::*")
    for product in productGrids:
        productHTML= (etree.tostring(product, pretty_print=True))
        tree = etree.parse(StringIO(productHTML),parser)
        image = tree.xpath("//div[@class='image']/a/img/@src")
        productLink= tree.xpath("//div[@class='name']/a/@href")
        name = tree.xpath("//div[@class='name']//text()")
        price = ''.join(tree.xpath("//span[@class='price-tax']/text()"))
        price=''.join(re.findall("([0-9]+,?[0-9]*\.?[0-9]*)*",price)).replace(',','')        
        description = tree.xpath("//div[@class='description']//text()")
        scraperwiki.sqlite.save(unique_keys=['productLink'], data={'productLink':''.join(productLink),'productName':''.join(name), 'price':''.join(price), 'description':''.join(description),'image':''.join(image)})

        
'''
'''
search = "site:yeskantipur.com"

for myI in range(10):
    startVal = myI*10+1
    strAddr = "https://www.googleapis.com/customsearch/v1?key=AIzaSyAu0Qjk8EhHfIZwZ5zRxeCYvRIt3M1DsjE&cx=013954637796931996224:b03wibgo-gq&start="+str(startVal)+"&q="+search
   
    html = urllib.urlopen(strAddr)
    Json = html.read()
    print Json
    output = json.loads(Json)
    message =""
    items = output['items']  or [] 
    for item in items:
        givenLink = item['link']
        #givenLink ="http://www.yeskantipur.com/index.php?route=product/product&product_id=3257"
    
        #html=scraperwiki.scrape(givenLink)
        html = urllib.urlopen(givenLink)
        html = html.read()
    
        parser = etree.HTMLParser()
        tree   = etree.parse(StringIO(html), parser)
    
        productNames=tree.xpath("//div[@class='product_title']/h1/text()")
        productName=""
        for pName in productNames:
            productName= pName
        prices= tree.xpath("//div[@class='price']/text()")
        price =""
        for prc in prices:
            price = prc
            price = price.replace("Price: ","").lstrip()
    
        if price=='':
            prices=tree.xpath("//div[@class='price']/span[@class='price-new']/text()")
            for prc in prices:
                price = prc
                price = price.replace("Price: ","").lstrip()
        
        description = tree.xpath("//div[@id='tab-description']//text()")
        message += productName + price
        for desc in description:
            desc+= " "+desc
        scraperwiki.sqlite.save(unique_keys=['link'], data={'link':givenLink,'productName':productName, 'price':price, 'description':description})

'''
