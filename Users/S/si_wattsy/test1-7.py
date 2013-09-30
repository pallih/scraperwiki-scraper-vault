# 205 55 16

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

url= 'http://www.camskill.co.uk/products.php?plid=m12b0s677p0'
html = scraperwiki.scrape(url)
print html

soup = BeautifulSoup(html)

tds = soup.findAll('td') 
for td in tds:

    ProdID = '-1'
    ProdName = '-1'
    ProdPrice = '-1'

    inputs = td.findAll('input')

    for input in inputs :
        if input['name'] == 'productName':
            ProdName = input['value']
        if input['name'] == 'productPrice':
            ProdPrice = input['value']
        if input['name'] == 'productID':
            ProdID = input['value']

    if ProdName != '-1' :
        if ProdPrice != '-1' :
            if ProdID != '-1' :
                record = { "row" : ProdID + ', ' + ProdName + ', ' + ProdPrice} # column name and value
                scraperwiki.datastore.save(["row"], record) # save the records one by one
                print ProdID + ', ' + ProdName + ', ' + ProdPrice
            

# 205 55 16

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

url= 'http://www.camskill.co.uk/products.php?plid=m12b0s677p0'
html = scraperwiki.scrape(url)
print html

soup = BeautifulSoup(html)

tds = soup.findAll('td') 
for td in tds:

    ProdID = '-1'
    ProdName = '-1'
    ProdPrice = '-1'

    inputs = td.findAll('input')

    for input in inputs :
        if input['name'] == 'productName':
            ProdName = input['value']
        if input['name'] == 'productPrice':
            ProdPrice = input['value']
        if input['name'] == 'productID':
            ProdID = input['value']

    if ProdName != '-1' :
        if ProdPrice != '-1' :
            if ProdID != '-1' :
                record = { "row" : ProdID + ', ' + ProdName + ', ' + ProdPrice} # column name and value
                scraperwiki.datastore.save(["row"], record) # save the records one by one
                print ProdID + ', ' + ProdName + ', ' + ProdPrice
            

