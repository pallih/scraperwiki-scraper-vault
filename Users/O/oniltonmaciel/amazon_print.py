import scraperwiki
import lxml.html
import time
from random import shuffle

mainUrl="http://www.amazonprint.com.br/"

categoryFinder="ul.menu li:not(.parent) > a"

#categoryUrlTransformer={
#'source' : ''
#}

paginationFinder="div.toolbar-bottom > div.toolbar div.pages li > a"

productFinder="div.products-container a"

productInfoFinder={
'name' : 'div.product-name > h1 ',
'price' : 'span.price',
'detail' : 'div#box-description > div.std',
'image_url' : 'p.product-image img' 
}

sleepForEachCategory=2
sleepForEachProduct=0.1



html = scraperwiki.scrape(mainUrl)
#print html
root = lxml.html.fromstring(html)

categoriesFound = root.cssselect(categoryFinder)
shuffle(categoriesFound)

#Get the category links
for alink in categoriesFound:
    time.sleep(sleepForEachCategory)
    #print alink.text_content(),alink.get('href')
    categoryUrl=alink.get('href')    
    print 'Cateogryurl',categoryUrl

    categoryPage = scraperwiki.scrape(categoryUrl)
    rootCategoryPage = lxml.html.fromstring(categoryPage)
    #todo improve page limits. 
    for productLink in rootCategoryPage.cssselect(productFinder):
        #print productLink.text_content(),productLink.get('href')
        #######print 'url',productLink.get('href')
        time.sleep(sleepForEachProduct)
        productUrl=productLink.get('href')

        productPage = scraperwiki.scrape(productUrl)        
        rootProductPage = lxml.html.fromstring(productPage)
        prodData={}
        prodData['url']=productUrl
        for pInfoName, pInfoFinder in productInfoFinder.iteritems():
            #print pInfoName,pInfoFinder
            prodElementData=rootProductPage.cssselect(pInfoFinder)
            if len(prodElementData)>=1:
                if pInfoName=='image_url':
                    #print pInfoName,prodElementData[0].get('src')
                    prodData[pInfoName]=prodElementData[0].get('src')
                else:
                    #print pInfoName,prodElementData[0].text_content()
                    prodData[pInfoName]=prodElementData[0].text_content()
            #else:
            #    print pInfoName,""
            #    prodData[pInfoName]=prodElementData[0].text_content()
            scraperwiki.sqlite.save(unique_keys=['url'], data=prodData)

    for paginationItem in rootCategoryPage.cssselect(paginationFinder):
        print "Pagina",paginationItem.text_content()
        paginationUrl=paginationItem.get('href')

        categoryPage = scraperwiki.scrape(paginationUrl)
        rootCategoryPage = lxml.html.fromstring(categoryPage)
        #todo improve page limits. 
        for productLink in rootCategoryPage.cssselect(productFinder):
            #print productLink.text_content(),productLink.get('href')
            #####print 'url',productLink.get('href')
            time.sleep(sleepForEachProduct)
            productUrl=productLink.get('href')
    
            productPage = scraperwiki.scrape(productUrl)        
            rootProductPage = lxml.html.fromstring(productPage)
            prodData={}
            prodData['url']=productUrl
            for pInfoName, pInfoFinder in productInfoFinder.iteritems():
                #print pInfoName,pInfoFinder
                prodElementData=rootProductPage.cssselect(pInfoFinder)
                if len(prodElementData)>=1:
                    if pInfoName=='image_url':
                        #print pInfoName,prodElementData[0].get('src')
                        prodData[pInfoName]=prodElementData[0].get('src')
                    else:
                        #print pInfoName,prodElementData[0].text_content()
                        prodData[pInfoName]=prodElementData[0].text_content()
                #else:
                #    print pInfoName,""
                #    prodData[pInfoName]=prodElementData[0].text_content()
                scraperwiki.sqlite.save(unique_keys=['url'], data=prodData)
