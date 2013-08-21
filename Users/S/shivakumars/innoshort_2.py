import scraperwiki
import lxml.html           

html = scraperwiki.scrape("http://shortz.in/directory")
root = lxml.html.fromstring(html)

#Temporary Storage Arrays
dataCategories=[]

sepPanel=root.cssselect("div.item-list")

for el in sepPanel:
    categories=lxml.html.fromstring(lxml.html.tostring(el)).cssselect("h3 a")
    if len(categories)>0:
        dataTypes=[]
        dataNumber=[]
        types=lxml.html.fromstring(lxml.html.tostring(el)).cssselect("ul li span a")
        for i in types:
            dataTypes.append(i.text)
            #print i.text
        number=lxml.html.fromstring(lxml.html.tostring(el)).cssselect("ul li span span.directory-nodecount")
        for i in number:
            dataNumber.append(i.text)
            #print i.text
        data={
        'category':categories[0].text,
        'subCate':dataTypes,
        'noOfMoviesInEachSubCate':dataNumber
        }
        scraperwiki.sqlite.save(unique_keys=['category'], data=data)
        print 'break'



