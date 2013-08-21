import scraperwiki
import sys
from bs4 import BeautifulSoup

searches = [
"http://www.chubbyscruisers.com/shop/firmstrong-diva",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-girls-20",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-boys-20",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-boutique",
"http://www.chubbyscruisers.com/shop/firmstrong-bella-classic",
"http://www.chubbyscruisers.com/shop/firmstrong-diva",
"http://www.chubbyscruisers.com/shop/nirve-mens-starliner-21-7-spd",
"http://www.chubbyscruisers.com/shop/firmstrong-mens-urban-3-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-shimano",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-alloy-0",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-alloy",
"http://www.chubbyscruisers.com/shop/firmstrong-bruiser",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-lrd",
"http://www.chubbyscruisers.com/shop/firmstrong-bella-fashionista",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-shimano-0",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-shimano",
"http://www.chubbyscruisers.com/shop/mens-high-roller-29er-single-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-chief-forward-pedaling",
"http://www.chubbyscruisers.com/shop/firmstrong-womens-chief",
"http://www.chubbyscruisers.com/shop/firmstrong-mens-urban-7-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-womens-urban-7-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-ca-520-7-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-mens-urban-3-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-womens-24-urban-3-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-mens-urban-3-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-bella-3-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-womens-24-urban-3-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-deluxe",
"http://www.chubbyscruisers.com/shop/firmstrong-rebel",
"http://www.chubbyscruisers.com/shop/firmstrong-bruiser-7-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-bella-7-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-girls-20",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-girls-20",
"http://www.chubbyscruisers.com/shop/firmstrong-bruiser",
"http://www.chubbyscruisers.com/shop/firmstrong-chief-3-speed-forward-pedaling",
"http://www.chubbyscruisers.com/shop/firmstrong-26-bicycle-fender-set",
"http://www.chubbyscruisers.com/shop/girls-20-sachi-single-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-chief-3-speed-forward-pedaling",
"http://www.chubbyscruisers.com/shop/mens-sea-crest-deluxe-noir-single-speed",
"http://www.chubbyscruisers.com/shop/firmstrong-urban-girls-20"]

for search in searches:
    html = scraperwiki.scrape(search)
    soup = BeautifulSoup(html)
    #print soup
    maindiv = soup.find_all(id='productDetailsTop')
    #print maindiv
    pr = maindiv[0].find('div', {"class":"productRegPrice"}).text
    if pr:
        print pr
        data = {}
        data['URL'] = search
        data['price'] = pr
        scraperwiki.sqlite.save(unique_keys=["URL"], data={"URL":search, "price":pr}) 
    else:
        print 'nodata'
        data = {}
        data['URL'] = search
        data['price'] = 'nodata'
        scraperwiki.sqlite.save(unique_keys=["URL"], data={"URL":search, "price":pr})         

print scraperwiki.sqlite.show_tables()

#for link in pr:
        #url = link["href"]
#        print link
        #data = {"URL":url}
        #scraperwiki.sqlite.save(["URL"], data)
