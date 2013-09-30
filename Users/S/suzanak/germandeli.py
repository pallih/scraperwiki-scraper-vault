import scraperwiki

from bs4 import BeautifulSoup

import urllib
import random
import datetime

url = "http://www.germandeli.com/newproducts.html"
baseurl = "http://www.germandeli.com/"
blocked = ["newproducts.html", "backinstock.html", "schnaeppchen.html", "index-recipes.html"]

# THESE LINKS ARE NOT PERSISTENT - CHECK BEFORE AND CHANGE THEM IF NECESSARY
# 1 = non-perishable
# 2 = heat-sensitive
# 3 = refrigerated
# 4 = frozen item 
perishable = {'http://ep.yimg.com/ca/I/gdcom_2254_1540285':'non-perishable', 'http://ep.yimg.com/ca/I/gdcom_2254_611872':'heat-sensitive', \
'http://ep.yimg.com/ca/I/gdcom_2254_8934395':'refrigerated', 'http://ep.yimg.com/ca/I/gdcom_2254_1704229':'frozen item'}


def get_newproduct_links():

    # open website
    fh = urllib.urlopen(url)
    # read website 
    html = fh.read()
    soup = BeautifulSoup(html)
    contents = soup.find(id='contents')
    links = contents.find_all('a')
    links = [a['href'] for a in links if a['href'] not in blocked]
    
    return links


# scraperwiki needs a liste of dictionaries to save the data as sqlite tabel

def get_newproduct_data(links):

    this_day = datetime.date.today().isoformat()
    data = []
    for l in links[51:]:
        #print baseurl+l 
        #try:          
            linkdata = {}
            # webseite oeffnen
            fh = urllib.urlopen(baseurl+l)
            # webseite einlesen
            html = fh.read()
            soup = BeautifulSoup(html)
            
            linkdata['name'] = soup.title.text
            print linkdata['name']
            div = soup.select(".item-images")
            if div:
                img = div[0]
                linkdata['image-link'] = img.img['src']
                #print linkdata['image-link']
            
            div = soup.select('.brand')
            #print div
            if div:
                td = div[0].find('td')
                if td:
                     linkdata['brand'] = td.text
                

            div = soup.select('.countryoforigin')
            if div:

                linkdata['country'] = div[0].td.text
                #print linkdata['country']

            div = soup.select('.weight')
            if div:
                linkdata['weight'] =  div[0].td.text

            div = soup.select('.sale-price')
            if div:
                linkdata['price'] =  div[0].td.text
                #print linkdata['price']

            div = soup.select('.code')
            if div:
                linkdata['id'] =  div[0].td.text
                #print linkdata['id']

            linkdata['product-link'] = l

            div = soup.select('.perishable')
            if div:
                 perishable_div = div[0]
                 perishable_image = perishable_div.find('img')            
                 perishable_image_link = perishable_image.get('src')
                 if perishable_image_link:
                     perishable_data = perishable.get(perishable_image_link)
                     if perishable_data:
                         linkdata['perishable'] = perishable_data
                         print perishable_data
                     else:
                         print 'unknown image link for perishable data!'
                 else: 
                     print 'unknown if object is perishable!'

            div = soup.select('.scBreadcrumbs')
            if div:
                 breadcrumps = div[0]
                 taxonomy = [a.text for a in breadcrumps.find_all('a')]
                 linkdata['taxonomy'] =  " > ".join(taxonomy[1:])

            toolboxes = soup.select('.infobox')
            for t in toolboxes:
                 toolbox_name = t['name']
                 linkdata[toolbox_name] = t.text
            

            data.append(linkdata)
            print linkdata
            scraperwiki.sqlite.save(unique_keys=['id'], data=linkdata, table_name="newproducts")

        #except:
            #print "ERROR!" 

    return data


links = get_newproduct_links()
data = get_newproduct_data(links)


import scraperwiki

from bs4 import BeautifulSoup

import urllib
import random
import datetime

url = "http://www.germandeli.com/newproducts.html"
baseurl = "http://www.germandeli.com/"
blocked = ["newproducts.html", "backinstock.html", "schnaeppchen.html", "index-recipes.html"]

# THESE LINKS ARE NOT PERSISTENT - CHECK BEFORE AND CHANGE THEM IF NECESSARY
# 1 = non-perishable
# 2 = heat-sensitive
# 3 = refrigerated
# 4 = frozen item 
perishable = {'http://ep.yimg.com/ca/I/gdcom_2254_1540285':'non-perishable', 'http://ep.yimg.com/ca/I/gdcom_2254_611872':'heat-sensitive', \
'http://ep.yimg.com/ca/I/gdcom_2254_8934395':'refrigerated', 'http://ep.yimg.com/ca/I/gdcom_2254_1704229':'frozen item'}


def get_newproduct_links():

    # open website
    fh = urllib.urlopen(url)
    # read website 
    html = fh.read()
    soup = BeautifulSoup(html)
    contents = soup.find(id='contents')
    links = contents.find_all('a')
    links = [a['href'] for a in links if a['href'] not in blocked]
    
    return links


# scraperwiki needs a liste of dictionaries to save the data as sqlite tabel

def get_newproduct_data(links):

    this_day = datetime.date.today().isoformat()
    data = []
    for l in links[51:]:
        #print baseurl+l 
        #try:          
            linkdata = {}
            # webseite oeffnen
            fh = urllib.urlopen(baseurl+l)
            # webseite einlesen
            html = fh.read()
            soup = BeautifulSoup(html)
            
            linkdata['name'] = soup.title.text
            print linkdata['name']
            div = soup.select(".item-images")
            if div:
                img = div[0]
                linkdata['image-link'] = img.img['src']
                #print linkdata['image-link']
            
            div = soup.select('.brand')
            #print div
            if div:
                td = div[0].find('td')
                if td:
                     linkdata['brand'] = td.text
                

            div = soup.select('.countryoforigin')
            if div:

                linkdata['country'] = div[0].td.text
                #print linkdata['country']

            div = soup.select('.weight')
            if div:
                linkdata['weight'] =  div[0].td.text

            div = soup.select('.sale-price')
            if div:
                linkdata['price'] =  div[0].td.text
                #print linkdata['price']

            div = soup.select('.code')
            if div:
                linkdata['id'] =  div[0].td.text
                #print linkdata['id']

            linkdata['product-link'] = l

            div = soup.select('.perishable')
            if div:
                 perishable_div = div[0]
                 perishable_image = perishable_div.find('img')            
                 perishable_image_link = perishable_image.get('src')
                 if perishable_image_link:
                     perishable_data = perishable.get(perishable_image_link)
                     if perishable_data:
                         linkdata['perishable'] = perishable_data
                         print perishable_data
                     else:
                         print 'unknown image link for perishable data!'
                 else: 
                     print 'unknown if object is perishable!'

            div = soup.select('.scBreadcrumbs')
            if div:
                 breadcrumps = div[0]
                 taxonomy = [a.text for a in breadcrumps.find_all('a')]
                 linkdata['taxonomy'] =  " > ".join(taxonomy[1:])

            toolboxes = soup.select('.infobox')
            for t in toolboxes:
                 toolbox_name = t['name']
                 linkdata[toolbox_name] = t.text
            

            data.append(linkdata)
            print linkdata
            scraperwiki.sqlite.save(unique_keys=['id'], data=linkdata, table_name="newproducts")

        #except:
            #print "ERROR!" 

    return data


links = get_newproduct_links()
data = get_newproduct_data(links)


