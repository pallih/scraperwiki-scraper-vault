import scraperwiki
import lxml.html
import math


html = scraperwiki.scrape("http://www.greenpeace.org/international/en/news/")
root = lxml.html.fromstring(html)

results =root.cssselect("div.result-pages strong")[1]
print(results.text)
numberofpages = float(results.text)/float(15)
numberofpages = int(math.ceil(numberofpages))
print(numberofpages)

for i in range(0, numberofpages):
    html2 = scraperwiki.scrape("http://www.greenpeace.org/international/en/news/?page="+str(i))
    root2 = lxml.html.fromstring(html2)
    print("http://www.greenpeace.org/international/en/news/?page="+str(i))
 #   print(root2)
    data ={}
    cats = ''
    for el in root2.cssselect("div.news-content a"):
 #       print el.attrib['href']
        if "#comments-holder" in el.attrib['href']:
            pass
        else:
            if "http" in el.attrib['href']:
                html2 = scraperwiki.scrape(el.attrib['href'])  
            else:
                html2 = scraperwiki.scrape("http://www.greenpeace.org"+ el.attrib['href'])   
                root2 = lxml.html.fromstring(html2)
                data['link'] = "http://www.greenpeace.org"+ el.attrib['href']
                headline = root2.cssselect("html body.article form#aspnetForm div.page div#wrapper div#main div#content div.happen-box h1 span")
                
                print("headline" +str(headline))
                print(type(headline))
                for i in headline:
                    data['title'] = i.text
#            print("http://www.greenpeace.org"+ el.attrib['href'])
                date = root2.cssselect("html body.article form#aspnetForm div.page div#wrapper div#main div#content div.happen-box div.happen-content div.text span.author")
                for i in date:
                    data['date'] = i.text.split(" - ")[1]


                leader = root2.cssselect("html body.article form#aspnetForm div.page div#wrapper div#main div#content div.happen-box div.happen-content div.text div.leader div")
                for i in leader:
                    data['text'] = i.text

                catstring = ""    
                for el in root2.cssselect("div.tags a"):
                    catstring += el.attrib['title']+ ", "
                    data['cats'] = catstring[:-2]
                print(catstring[:-2])
                scraperwiki.sqlite.save(unique_keys=['link'], data=data)
