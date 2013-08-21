import scraperwiki
import json #for json decoding
from lxml import etree     
from cStringIO import StringIO
import urllib

import re


strAddr = "http://www.yeskantipur.com/index.php?route=information/sitemap"
html = urllib.urlopen(strAddr)
html = html.read()
parser = etree.HTMLParser()
tree   = etree.parse(StringIO(html), parser)
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