import scraperwiki
import lxml.html
import math


html = scraperwiki.scrape("http://www.greenpeace.org/international/en/multimedia/videos/")
root = lxml.html.fromstring(html)

results =root.cssselect("div.result-pages strong")[1]
#print(results.text)
numberofpages = float(results.text)/float(12)
numberofpages = int(math.ceil(numberofpages))
#print(numberofpages)

for i in range(0, numberofpages):
    html2 = scraperwiki.scrape("http://www.greenpeace.org/international/en/multimedia/videos/?page="+str(i))
    root2 = lxml.html.fromstring(html2)
    print("http://www.greenpeace.org/international/en/multimedia/videos/?page="+str(i))
#    print(root2)
    data ={}
    cats = ''
    for el in root2.cssselect("div.gallery-wrapper a"):
#        print el.attrib['href']
        html2 = scraperwiki.scrape("http://www.greenpeace.org"+ el.attrib['href'])   
        print("http://www.greenpeace.org"+ el.attrib['href'])
        root2 = lxml.html.fromstring(html2)
    #    headline = root2.cssselect("div.promo general-form h2")
    #    print("headline: "+headline)
        description =root2.cssselect("div.'text video-text' p")
        data['text'] = description[0].text

        title = root2.cssselect("div.'promo general-form' span")
        data['title'] = title[0].text
        print(title[1].text)
        data['date'] = title[1].text.split("| ")[1]
        video = root2.cssselect("div.embedinfo-video input")
        data['link'] = video[0].attrib['value']
#           data = {
 #               'title' : picture.attrib['title'],
  #              'text' : picture.attrib['rel'],
   #             'link' : picture.attrib['href']
    #        }
            
#            print(picture.attrib['title'])
#            print(picture.attrib['rel'])
#            print(picture.attrib['href'])
        
    #    i = 0    
   #     for el in root2.cssselect("div.tags a"):
  #          data['cat'+str(i)] = el.attrib['title']
 #           i = i+1
        catstring = "" 
        for el in root2.cssselect("div.tags a"):
            catstring += el.attrib['title']+ ", "
        data['cats'] = catstring[:-2]
        print(catstring[:-2])

        scraperwiki.sqlite.save(unique_keys=['link'], data=data)
import scraperwiki
import lxml.html
import math


html = scraperwiki.scrape("http://www.greenpeace.org/international/en/multimedia/videos/")
root = lxml.html.fromstring(html)

results =root.cssselect("div.result-pages strong")[1]
#print(results.text)
numberofpages = float(results.text)/float(12)
numberofpages = int(math.ceil(numberofpages))
#print(numberofpages)

for i in range(0, numberofpages):
    html2 = scraperwiki.scrape("http://www.greenpeace.org/international/en/multimedia/videos/?page="+str(i))
    root2 = lxml.html.fromstring(html2)
    print("http://www.greenpeace.org/international/en/multimedia/videos/?page="+str(i))
#    print(root2)
    data ={}
    cats = ''
    for el in root2.cssselect("div.gallery-wrapper a"):
#        print el.attrib['href']
        html2 = scraperwiki.scrape("http://www.greenpeace.org"+ el.attrib['href'])   
        print("http://www.greenpeace.org"+ el.attrib['href'])
        root2 = lxml.html.fromstring(html2)
    #    headline = root2.cssselect("div.promo general-form h2")
    #    print("headline: "+headline)
        description =root2.cssselect("div.'text video-text' p")
        data['text'] = description[0].text

        title = root2.cssselect("div.'promo general-form' span")
        data['title'] = title[0].text
        print(title[1].text)
        data['date'] = title[1].text.split("| ")[1]
        video = root2.cssselect("div.embedinfo-video input")
        data['link'] = video[0].attrib['value']
#           data = {
 #               'title' : picture.attrib['title'],
  #              'text' : picture.attrib['rel'],
   #             'link' : picture.attrib['href']
    #        }
            
#            print(picture.attrib['title'])
#            print(picture.attrib['rel'])
#            print(picture.attrib['href'])
        
    #    i = 0    
   #     for el in root2.cssselect("div.tags a"):
  #          data['cat'+str(i)] = el.attrib['title']
 #           i = i+1
        catstring = "" 
        for el in root2.cssselect("div.tags a"):
            catstring += el.attrib['title']+ ", "
        data['cats'] = catstring[:-2]
        print(catstring[:-2])

        scraperwiki.sqlite.save(unique_keys=['link'], data=data)
