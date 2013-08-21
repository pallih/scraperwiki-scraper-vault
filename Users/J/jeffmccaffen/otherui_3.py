import resource
import scraperwiki
import lxml.html
import sys


url = 'http://inspired-ui.com/page/1'
while True:
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for post in root.cssselect(".posts"): 
        img = post.cssselect(".post-frame img")[0].attrib.get('src')
        appDetailURL = post.cssselect(".caption a")[0].attrib.get('href')
        appName = post.cssselect('.caption a')[0].text_content()
        _category = post.cssselect('.tags')[0].text_content()

        appShortName = ((post.cssselect(".post-frame img")[0].attrib.get('alt')).lower()).replace(' ', '')
        _category  = _category.replace('app '+ appShortName, '')
        _category = _category.replace(appShortName, '')
        _category = _category.split('|')
        category = filter(None, _category)

        data = {
            'imgURL' : img,
            'appDetailURL' : appDetailURL,
            'appName' : appName,
            'appShortName' : appShortName,
            'category' : category
        }
        
        # print data
        scraperwiki.sqlite.save(unique_keys=[], data=data)

    
    try:
        url = 'http://inspired-ui.com' + root.cssselect(".pagination a:last-child")[0].attrib.get('href')
        print 'Parsing ' + url + '...'
    
    except:
        print "Error, cannot find next page"
        break        
        raise

    
