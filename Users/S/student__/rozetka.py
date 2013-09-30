import scraperwiki
import lxml.html 
url="http://rozetka.com.ua/mobile-phones/c80003/filter/" 
iter=1 
page=url
while True: 
    print page
    iter = iter+1
    html = scraperwiki.scrape(page) 
    root = lxml.html.fromstring(html)

    middle = root.cssselect("div.c-middle div")[0]
    goods = middle.cssselect("div.goods.list div")
    for i in goods:
        try:
            print i.cssselect("div.title")[0].text_content()
            print i.cssselect("table.price-label")[0].text_content()
            price = i.cssselect("div.uah")[0].text_content()
            print price
            title = i.cssselect("div.title")[0].text_content()
            mydata = { 'model':title, 'price': price}
            scraperwiki.sqlite.save(unique_keys=['model'], data=mydata)
        except:
            print 1

        
    page = url+"page="+str(iter)+"/"
    if iter>10:
        breakimport scraperwiki
import lxml.html 
url="http://rozetka.com.ua/mobile-phones/c80003/filter/" 
iter=1 
page=url
while True: 
    print page
    iter = iter+1
    html = scraperwiki.scrape(page) 
    root = lxml.html.fromstring(html)

    middle = root.cssselect("div.c-middle div")[0]
    goods = middle.cssselect("div.goods.list div")
    for i in goods:
        try:
            print i.cssselect("div.title")[0].text_content()
            print i.cssselect("table.price-label")[0].text_content()
            price = i.cssselect("div.uah")[0].text_content()
            print price
            title = i.cssselect("div.title")[0].text_content()
            mydata = { 'model':title, 'price': price}
            scraperwiki.sqlite.save(unique_keys=['model'], data=mydata)
        except:
            print 1

        
    page = url+"page="+str(iter)+"/"
    if iter>10:
        break