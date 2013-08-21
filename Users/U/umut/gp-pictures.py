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

for i in range(28, numberofpages):
    html2 = scraperwiki.scrape("http://www.greenpeace.org/international/en/multimedia/photos/?page="+str(i))
    root2 = lxml.html.fromstring(html2)
    print("http://www.greenpeace.org/international/en/multimedia/photos/?page="+str(i))
    print(root2)
    data ={}
    cats = ''
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
        data['source'] = "http://www.greenpeace.org"+ el.attrib['href']
        title = root2.cssselect("div.'promo general-form' span")
        print(title)
        print(title[0].text.split("| ")[1])
        data['date'] = title[0].text.split("| ")[1]     
#            print(picture.attrib['title'])
#            print(picture.attrib['rel'])
#            print(picture.attrib['href'])
        
        i = 0
        catstring = ""    
        for el in root2.cssselect("div.tags a"):
            catstring += el.attrib['title']+ ", "
        data['cats'] = catstring[:-2]
        print(catstring[:-2])
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)
