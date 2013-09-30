import scraperwiki
import lxml.html
import sys
class PageInfo:
    def __init__(self, pageName, categoryName):
        self.page = pageName
        self.category = categoryName

#collect data
def collectData():
    webpages = []
    urls = []
    print "collecting category urls...."
    for x in range(0, 204):
        url2 = "http://www.sikayetim.com/module.php?cat=" + str(x)+ "&startat=0&mul=0"
        html = scraperwiki.scrape(url2)   
        root = lxml.html.fromstring(html)
        listp = root.cssselect("div [class='breadcrumb'] b")
        numberofpage = 0
        if len(listp)!= 0:
            numberofpage = listp[1].text_content()
        for i in range(0, int(numberofpage)):
            url = "http://www.sikayetim.com/module.php?cat=" + str(x)+ "&startat=" + str(12*i) + "&mul=0"
            urls.append(url)

    print "collecting detail urls..."
    i = 28417
    for url in urls:
        html = scraperwiki.scrape(url)   
        root = lxml.html.fromstring(html)
        listp = root.cssselect("div[id='sblock'] p[style='padding-left:10px;'] a")
        category = root.cssselect("div[id='sblock'] p[class='breadcrumb'] b a[onclick='']")
        if len(category) != 0:
            c = category[0].text_content()
        for l in listp:
            page = "http://www.sikayetim.com/" + l.attrib.get('href')
            p = PageInfo(page,c)
            url = p.page
            category = p.category
            html =  scraperwiki.scrape(url)    
            root = lxml.html.fromstring(html)
            select = root.cssselect("div [class='tablehead'] h2")
            select2 = root.cssselect("table[border='0']  tr td[colspan='4']")
            if len(select2)>0 and len(select)>0:
                info = select2[0].text_content().encode('utf-8')
                op = select[0].text_content().encode('utf-8')
                data = { 'id' : i, 'category' : category, 'opinion' : op, 'detail' : info }
                scraperwiki.sqlite.save(unique_keys=['id'], data=data,  table_name="sikayetler")
                i = i + 1

collectData()


import scraperwiki
import lxml.html
import sys
class PageInfo:
    def __init__(self, pageName, categoryName):
        self.page = pageName
        self.category = categoryName

#collect data
def collectData():
    webpages = []
    urls = []
    print "collecting category urls...."
    for x in range(0, 204):
        url2 = "http://www.sikayetim.com/module.php?cat=" + str(x)+ "&startat=0&mul=0"
        html = scraperwiki.scrape(url2)   
        root = lxml.html.fromstring(html)
        listp = root.cssselect("div [class='breadcrumb'] b")
        numberofpage = 0
        if len(listp)!= 0:
            numberofpage = listp[1].text_content()
        for i in range(0, int(numberofpage)):
            url = "http://www.sikayetim.com/module.php?cat=" + str(x)+ "&startat=" + str(12*i) + "&mul=0"
            urls.append(url)

    print "collecting detail urls..."
    i = 28417
    for url in urls:
        html = scraperwiki.scrape(url)   
        root = lxml.html.fromstring(html)
        listp = root.cssselect("div[id='sblock'] p[style='padding-left:10px;'] a")
        category = root.cssselect("div[id='sblock'] p[class='breadcrumb'] b a[onclick='']")
        if len(category) != 0:
            c = category[0].text_content()
        for l in listp:
            page = "http://www.sikayetim.com/" + l.attrib.get('href')
            p = PageInfo(page,c)
            url = p.page
            category = p.category
            html =  scraperwiki.scrape(url)    
            root = lxml.html.fromstring(html)
            select = root.cssselect("div [class='tablehead'] h2")
            select2 = root.cssselect("table[border='0']  tr td[colspan='4']")
            if len(select2)>0 and len(select)>0:
                info = select2[0].text_content().encode('utf-8')
                op = select[0].text_content().encode('utf-8')
                data = { 'id' : i, 'category' : category, 'opinion' : op, 'detail' : info }
                scraperwiki.sqlite.save(unique_keys=['id'], data=data,  table_name="sikayetler")
                i = i + 1

collectData()


