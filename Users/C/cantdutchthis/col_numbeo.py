import urllib 
from bs4 import BeautifulSoup 
from time import gmtime, strftime
import unicodedata
import scraperwiki
import datetime

html_link = "http://www.numbeo.com/cost-of-living/" 
html_page = urllib.urlopen(html_link).read() 
soup      = BeautifulSoup(html_page) 
table     = soup.findAll('td')

for td_index in range(len(table) - 5, len(table)): 
    anchors = table[td_index].findAll('a')
    for anchor in anchors:
        country_link      = html_link + "country_result.jsp?country=" + str(anchor.contents[0]) + '&displayCurrency=USD'
        country_html_page = urllib.urlopen(country_link)
        local_soup        = BeautifulSoup(country_html_page) 
        country           = anchor.contents[0] 
        if (len(local_soup.findAll('tr',{"class","tr_highlighted"})) == 23): 
            for product in local_soup.findAll('tr',{"class","tr_highlighted"}):
                price = product.findAll('td')[1].contents
                if ( len(price[0]) != 2 ):
                    price = float(unicodedata.normalize('NFKD', price[0]).encode('ascii','ignore').replace("$","").replace(",",""))
                    product = product.findAll('td')
                    product = product[0].contents[0] 
                    data = {'product' : product, 'price': price, 'country':country, 'ID': country+product}
                    scraperwiki.sqlite.save(unique_keys=['ID'], data=data)
        if (len(local_soup.findAll('tr',{"class","tr_standard"})) == 23): 
            for product in local_soup.findAll('tr',{"class","tr_highlighted"}):
                price = product.findAll('td')[1].contents
                if ( len(price[0]) != 2 ):
                    price = float(unicodedata.normalize('NFKD', price[0]).encode('ascii','ignore').replace("$","").replace(",",""))
                    product = product.findAll('td')
                    product = product[0].contents[0] 
                    data = {'product' : product, 'price': price, 'country':country, 'ID': datetime.now()}
                    scraperwiki.sqlite.save(unique_keys=['ID'], data=data)
