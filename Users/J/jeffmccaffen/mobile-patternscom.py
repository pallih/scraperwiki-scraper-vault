import resource
import scraperwiki
import lxml.html
import sys
import re


# Source Lists
baseURL = 'http://www.mobile-patterns.com'
html = scraperwiki.scrape(baseURL)
source = lxml.html.fromstring(html)

for parentCategory in source.cssselect("#sidebar .sidebar-item"):
    parentCategoryPath = parentCategory.cssselect("a")[0].attrib.get('href')
    parentCategoryName = parentCategory.text_content()
    
    url = baseURL + parentCategoryPath 
    
    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
        for pattern in root.cssselect(".pattern"): 
            tag = pattern.text_content()
            
            platform = re.search('\((.*?)\)',tag).group(1)
            appName = tag[:tag.find('(')] 

            img = pattern.cssselect("a:first-child")[0].attrib.get('href')

            _category = tag[(tag.find(')') + 1):]
            category = [x.strip() for x in _category.split(',')]

            data = {
                'imgURL' : img,
                'platform' : platform,
                'appName' : appName.strip(),
                'category' : category,
                'parentCategory' : parentCategoryName 
            }
        
            scraperwiki.sqlite.save(unique_keys=[], data=data)

    except:
        print "No more active URLs..."
        break        
        raise 

    
