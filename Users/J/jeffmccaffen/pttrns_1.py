import resource
import scraperwiki
import lxml.html
import sys

url = 'http://www.pttrns.com/?page=1'
while True:
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for article in root.cssselect(".pttrn.grid"): 
        img = article.cssselect("img")[0].attrib.get('data-retina-image')
        appDetailURL = 'http://www.pttrns.com' + article.cssselect("a")[0].attrib.get('href')
        appName = article.cssselect('.meta a')[0].text_content()
        category = article.cssselect('.category')[0].text_content()
    
        data = {
            'imgURL' : img,
            'appDetailURL' : appDetailURL,
            'appName' : appName,
            'category' : category
        }

        scraperwiki.sqlite.save(unique_keys=[], data=data)
    
    
    try:
        url = 'http://www.pttrns.com' + root.cssselect("a.next_page")[0].attrib.get('href')
        print 'Parsing ' + url + '...'
    
    except:
        print "Error, cannot find next page"
        raise
        break