###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_list(indus, starting_url):
    print starting_url
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    print html

#<a href="/en/US/products/hw/routers/ps133/index.html" class="contentboldlink">10000 Series Routers</a>
    rows = soup.findAll('a',{'class': 'contentboldlink'}) 
    for row in rows:
        record = {'title':None, 'content':None, 'source':None, 'imgUrl':None, 'date':None}
        
        record['product_name'] = row.text
        record['product_url'] = row.get('href')

        if len(record['product_name']) > 1:  
            print record
            scraperwiki.sqlite.save(unique_keys=['product_name'], data=record)



#http://www.forbes.com/global2000/list?page=1
pages=['prod_series_indexProduct_Series_Index_A.html',
'prod_series_indexProduct_Series_Index_B.html',
'prod_series_indexProdudct_Series_Index_C.html',
'prod_series_indexProdudct_Series_Index_D.html',
'prod_series_indexProdudct_Series_Index_E.html',
'prod_series_indexProdudct_Series_Index_F.html',
'prod_series_indexProdudct_Series_Index_I.html',
'prod_series_indexProdudct_Series_Index_L.html',
'prod_series_indexProdudct_Series_Index_M.html',
'prod_series_indexProdudct_Series_Index_N.html',
'prod_series_indexProdudct_Series_Index_S.html',
'prod_series_indexProdudct_Series_Index_W.html'
]

scrape_list('prod_series_index_listing_sitecopy.html','http://www.cisco.com/en/US/doctypes/prod_series_index_listing_sitecopy.html')

for i in range(len(pages)):
    scrape_list(pages[i],'http://www.cisco.com/en/US/products/'+pages[i])


###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_list(indus, starting_url):
    print starting_url
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    print html

#<a href="/en/US/products/hw/routers/ps133/index.html" class="contentboldlink">10000 Series Routers</a>
    rows = soup.findAll('a',{'class': 'contentboldlink'}) 
    for row in rows:
        record = {'title':None, 'content':None, 'source':None, 'imgUrl':None, 'date':None}
        
        record['product_name'] = row.text
        record['product_url'] = row.get('href')

        if len(record['product_name']) > 1:  
            print record
            scraperwiki.sqlite.save(unique_keys=['product_name'], data=record)



#http://www.forbes.com/global2000/list?page=1
pages=['prod_series_indexProduct_Series_Index_A.html',
'prod_series_indexProduct_Series_Index_B.html',
'prod_series_indexProdudct_Series_Index_C.html',
'prod_series_indexProdudct_Series_Index_D.html',
'prod_series_indexProdudct_Series_Index_E.html',
'prod_series_indexProdudct_Series_Index_F.html',
'prod_series_indexProdudct_Series_Index_I.html',
'prod_series_indexProdudct_Series_Index_L.html',
'prod_series_indexProdudct_Series_Index_M.html',
'prod_series_indexProdudct_Series_Index_N.html',
'prod_series_indexProdudct_Series_Index_S.html',
'prod_series_indexProdudct_Series_Index_W.html'
]

scrape_list('prod_series_index_listing_sitecopy.html','http://www.cisco.com/en/US/doctypes/prod_series_index_listing_sitecopy.html')

for i in range(len(pages)):
    scrape_list(pages[i],'http://www.cisco.com/en/US/products/'+pages[i])


