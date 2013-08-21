import scraperwiki

import re
import urllib2
from BeautifulSoup import BeautifulSoup

scraperwiki.sqlite.attach('fk_purl','purls')
purls = scraperwiki.sqlite.select('* from purls.swdata')

print purls

count = 0
shipping = "paid"

for purl in purls:
 price = 0
 url = purl['url']
 
 ProductPage = urllib2.urlopen(url)
 lines = ProductPage.readlines()
 
 for line in lines:
   match_title = re.search(r'<h1.*title="(.*)"',str(line))
   if match_title:
      title = match_title.group(1)
      print title
        
   list_price = re.search(r'fk-mprod-list-id">.{0,100}Rs\.[\s]+([\d]+)',str(line))
   if list_price:
      listprice = list_price.group(1)
      print listprice
        
   offer_price = re.search(r'fk-font-finalprice.*">.{0,100}Rs\.[\s]+([\d]+)',str(line))
   if offer_price:
      offerprice = offer_price.group(1)
      print offerprice
        
   match_stock = re.search(r'fk-stock-info-id.{0,5}>(\w+)',str(line))
   if match_stock:
      stock = match_stock.group(1)
      print stock

 sitecontent= urllib2.urlopen(url).read()
        
 site_bought = str(re.findall('class=".*carousel-title">(.*?)<script', sitecontent, re.S))
        
 print site_bought
        
 soup = BeautifulSoup(sitecontent)

 itemlist = soup.findAll('div', attrs={'class':'fk-two-line-title fks-bs-title'})
        
 soup2 = BeautifulSoup(sitecontent)

 pricelist = soup2.findAll('div', attrs={'class':'fk-price line rpadding3'})
        
 offerlist = site_bought.count('fk-price line rpadding3') 
        
 print len(itemlist), len(pricelist), offerlist
        
 z=1
        
 if len(itemlist)==len(pricelist):

  i=0

  while i <(len(itemlist)-offerlist):
     prod_name = itemlist[i].findAll(text=True)
     prod_listprice = pricelist[i].findAll('span', attrs={'class':'list-price'})
     for x in pricelist[i].findAll('span', attrs={'class':'price final-price'}):
          prod_offerprice = x.contents
     scraperwiki.sqlite.save(['id'],data={'id':z,'Prod_Name':title,'Url':url,'title':title,'Listprice':listprice,'Offerprice':offerprice,'stock':stock, 'type':"Viewed",'Associated_prod':prod_name, 'aListPrice':prod_listprice,'aOfferPrice':prod_offerprice})
     print i, title, listprice, offerprice, stock, prod_name, prod_listprice, prod_offerprice, '\n' 
     z=z+1
     i+=1
   
  while i <len(itemlist):    
     prod_name = itemlist[i].findAll(text=True)
     prod_listprice = pricelist[i].findAll('span', attrs={'class':'list-price'})
     for x in pricelist[i].findAll('span', attrs={'class':'price final-price'}):
         prod_offerprice = x.contents
     scraperwiki.sqlite.save(['id'],data={'id':z,'Prod_Name':title,'Url':url,'title':title,'Listprice':listprice,'Offerprice':offerprice,'stock':stock, 'type':"Bought",'Associated_prod':prod_name, 'aListPrice':prod_listprice,'aOfferPrice':prod_offerprice})
     print i, title, listprice, offerprice, stock, prod_name, prod_listprice, prod_offerprice, '\n' 
     z=z+1
     i+=1

 count = count + 1  







