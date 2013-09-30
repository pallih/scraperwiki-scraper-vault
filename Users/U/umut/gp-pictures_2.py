import scraperwiki
import lxml.html
import math


html = scraperwiki.scrape("http://www.greenpeace.org/international/en/multimedia/photos/")
root = lxml.html.fromstring(html)

results =root.cssselect("div.result-pages strong")[1]
#print(results.text)
numberofpages = float(results.text)/float(12)
numberofpages = int(math.ceil(numberofpages))
#print(numberofpages)

for i in range(1, numberofpages):
    html2 = scraperwiki.scrape("http://www.greenpeace.org/international/en/multimedia/photos/?page="+str(i))
    root2 = lxml.html.fromstring(html2)
    print("http://www.greenpeace.org/international/en/multimedia/photos/?page="+str(i))
    print(root2)
    for el in root2.cssselect("div.gallery-wrapper a"):
#        print el.attrib['href']
        html2 = scraperwiki.scrape("http://www.greenpeace.org"+ el.attrib['href'])   
        print("http://www.greenpeace.org"+ el.attrib['href'])
        root2 = lxml.html.fromstring(html2)
    #    headline = root2.cssselect("div.promo general-form h2")
    #    print("headline: "+headline)
        for picture in root2.cssselect("div.galleria_wrapper a"):
            data = {
                'title' : picture.attrib['title'],
                'text' : picture.attrib['rel'],
                'link' : picture.attrib['href']
            }
#            print(picture.attrib['title'])
#            print(picture.attrib['rel'])
#            print(picture.attrib['href'])
            scraperwiki.sqlite.save(unique_keys=['link'], data=data)
import scraperwiki
import lxml.html
import math


html = scraperwiki.scrape("http://www.greenpeace.org/international/en/multimedia/photos/")
root = lxml.html.fromstring(html)

results =root.cssselect("div.result-pages strong")[1]
#print(results.text)
numberofpages = float(results.text)/float(12)
numberofpages = int(math.ceil(numberofpages))
#print(numberofpages)

for i in range(1, numberofpages):
    html2 = scraperwiki.scrape("http://www.greenpeace.org/international/en/multimedia/photos/?page="+str(i))
    root2 = lxml.html.fromstring(html2)
    print("http://www.greenpeace.org/international/en/multimedia/photos/?page="+str(i))
    print(root2)
    for el in root2.cssselect("div.gallery-wrapper a"):
#        print el.attrib['href']
        html2 = scraperwiki.scrape("http://www.greenpeace.org"+ el.attrib['href'])   
        print("http://www.greenpeace.org"+ el.attrib['href'])
        root2 = lxml.html.fromstring(html2)
    #    headline = root2.cssselect("div.promo general-form h2")
    #    print("headline: "+headline)
        for picture in root2.cssselect("div.galleria_wrapper a"):
            data = {
                'title' : picture.attrib['title'],
                'text' : picture.attrib['rel'],
                'link' : picture.attrib['href']
            }
#            print(picture.attrib['title'])
#            print(picture.attrib['rel'])
#            print(picture.attrib['href'])
            scraperwiki.sqlite.save(unique_keys=['link'], data=data)
