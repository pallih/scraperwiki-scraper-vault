import scraperwiki
import lxml.html

# Blank Python

print 'hello, coding in the cloud'
html =  scraperwiki.scrape("http://t.co/bKJBePDx")

#print html

root = lxml.html.fromstring(html)

for imgs in root.cssselect("link"):

    
    temp = imgs.get('href')

    if temp and 'css' in temp:

        print temp[0: temp.index('.css')+4]

        data={
            'imgs': temp
        }


        scraperwiki.sqlite.save(unique_keys=['imgs'], data=data)import scraperwiki
import lxml.html

# Blank Python

print 'hello, coding in the cloud'
html =  scraperwiki.scrape("http://t.co/bKJBePDx")

#print html

root = lxml.html.fromstring(html)

for imgs in root.cssselect("link"):

    
    temp = imgs.get('href')

    if temp and 'css' in temp:

        print temp[0: temp.index('.css')+4]

        data={
            'imgs': temp
        }


        scraperwiki.sqlite.save(unique_keys=['imgs'], data=data)