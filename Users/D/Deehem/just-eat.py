import scraperwiki
import lxml.html



#functions

def getHTMLvalue(el, css, atr='text', index=0):
    try:
        lst = el.cssselect(css)
        val = ''
        if lst != None and len(lst) > 0:
            if index==0 or len(lst) >= index +1:
                if atr=='text':
                    val = lst[index].text_content()
                else:
                    val = lst[index].attrib.get(atr)
    
        return val
    except:
        return ''

baseurl = 'http://www.just-eat.co.uk'
postcodes = ['pr1']

for postcode in postcodes:
    url = 'http://www.just-eat.co.uk/area/' + postcode
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for restaurant in root.cssselect(".restaurantWithLogo"):
        record = {}
        record['name'] = getHTMLvalue(restaurant, "h3")
        link = getHTMLvalue(restaurant, "h3 a", "href")
        record['link'] = link
        record['url'] = baseurl + link
        record['address'] = getHTMLvalue(restaurant, "address")
        record['foodtype'] = getHTMLvalue(restaurant, '.restaurantCuisines').replace("Type of food", "")
        
        #get BT details

        scraperwiki.sqlite.save(['link'], record)
        #print name, link, address, foodtype