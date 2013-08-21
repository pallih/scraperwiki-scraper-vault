#!/usr/bin/env python
from urllib2 import urlopen
from csv import reader, writer
import scraperwiki
import csv
import lxml.html
from lxml import etree
from scraperwiki.sqlite import save, select
import BeautifulSoup
def select_mode():
    slist = ['sales','taxes','new_construction','foreclosures']
    
    mode = 1
    # scraper mode 
    # 1. sales
    # 2. taxes
    # 3. new homes
    # 4. foreclosures
    mode -= 1
    
    url="http://chicago.blockshopper.com/" + slist[mode]
        
    return url


# get all the data
def get_city_data(city_url_data):
    x = 1
    counter = 1
    while True:
        counter = 0
        while scraperwiki.scrape(city_url_data + "?page="+ str(x)):
            html = scraperwiki.scrape(city_url_data + "?page="+ str(x))
            city_data = lxml.html.fromstring(html)
            finalpage = True
            
            for tr in city_data.cssselect("table tbody tr"):
                
                #print tr.text_content().strip()
                if "Next" == tr.text_content().strip():
                    finalpage = False
                tds = tr.cssselect("td")
                print tds[0]   
                transaction = lxml.html.tostring(tds[0]).split('"')
                if len(transaction) < 2 :
                    transaction[1:] = ['']
                housetype = lxml.html.tostring(tds[2]).split('"')
                
                data = { 'Address'     : tds[2].text_content(),
                         'City'        : tds[3].text_content(),
                         'Type'        : housetype[1],
                         'Date'        : tds[1].text_content(),
                         'Price'       : tds[4].text_content(),
                         'Transaction' : transaction[1],
                         'Buyer'       : tds[5].text_content()
                        }
                scraperwiki.sqlite.save(unique_keys=['Address'],data=data)
                
                counter += 1
            
            #test for 2nd page
            
            
            a = city_data.cssselect("table tfoot")
            if a:
                b = lxml.html.tostring(a[0]).split('"')
                if len(b)>3:    
                    if b[7] == "next":
                        print (city_url_data + "?page="+ str(x))
                        x+=1    
                    else:
                        print (city_url_data + "?page="+ str(x)+ " ("+str(counter) + " entries).")
                        return
                else:
                    return
            else:
                return
            #if a:
            #   
                
            #    if b[3] == "next":
            #        x+=1
            #        break
            #    else:
            #        print(city_url_data + "?page="+ str(x)+ " ("+str(counter) + " entries).")
            #        return
            
          
        return

# get all the cities                                              
def get_cities(url):
    pagecounter = 1
    while scraperwiki.scrape(url + "?page="+ str(pagecounter)):
        html = scraperwiki.scrape(url + "?page="+ str(pagecounter)) 
        root = lxml.html.fromstring(html)
        for tr in root.cssselect(".sortable tbody tr"):
            tds = tr.cssselect("td")
                
            cityname = tds[0].text_content().strip()
            
            cityname = cityname.replace(" ","_") 
            cityname = cityname.replace("/","_")
            city_url_data = url+ "/cities/"+cityname+"/2012"
                
            get_city_data(city_url_data)
        
        pagecounter += 1                    
    return
# -- END --------                                              


print(get_cities(select_mode()))
