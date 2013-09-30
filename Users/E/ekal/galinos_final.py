# Scraping www.galinos.gr and creates a data set with all the drugs and their producers
import scraperwiki
import string, lxml.html
e=[]
allTheLetters = string.uppercase

for letter in allTheLetters:
    url="http://www.galinos.gr/web/drugs/main/lists/substances/%s#content" % (letter)
    page=lxml.html.fromstring(scraperwiki.scrape(url))
    for element in page.findall('.//div'):
        for uni in element.findall('.//td/a'):
            e.append(uni.get('href'))

# e.remove("some broken URLs")

            
for link in e:
    html = scraperwiki.scrape("http://www.galinos.gr%s" % (link))
    html = html.decode('utf-8')
    root = lxml.html.fromstring(html)
    for element in root.findall('.//tbody'):
        for tr in element.findall('.//tr'):
            for uni in tr.findall('.//td/a'):
                if uni.get('href').count('drugs') == 2:
                    x = uni.text_content()
                if uni.get('href').count('companies') == 1:
                    y = uni.text_content()    
                    data = {            
                        'drug' : x,
                        'company' : y
                    }  
                    print data
                    scraperwiki.sqlite.save(unique_keys=[], data=data)# Scraping www.galinos.gr and creates a data set with all the drugs and their producers
import scraperwiki
import string, lxml.html
e=[]
allTheLetters = string.uppercase

for letter in allTheLetters:
    url="http://www.galinos.gr/web/drugs/main/lists/substances/%s#content" % (letter)
    page=lxml.html.fromstring(scraperwiki.scrape(url))
    for element in page.findall('.//div'):
        for uni in element.findall('.//td/a'):
            e.append(uni.get('href'))

# e.remove("some broken URLs")

            
for link in e:
    html = scraperwiki.scrape("http://www.galinos.gr%s" % (link))
    html = html.decode('utf-8')
    root = lxml.html.fromstring(html)
    for element in root.findall('.//tbody'):
        for tr in element.findall('.//tr'):
            for uni in tr.findall('.//td/a'):
                if uni.get('href').count('drugs') == 2:
                    x = uni.text_content()
                if uni.get('href').count('companies') == 1:
                    y = uni.text_content()    
                    data = {            
                        'drug' : x,
                        'company' : y
                    }  
                    print data
                    scraperwiki.sqlite.save(unique_keys=[], data=data)