import scraperwiki
import lxml.html


# Blank Python
# work in progress

html = scraperwiki.scrape("http://hackshackers.com/chapters/")
root = lxml.html.fromstring(html)
temp = root.cssselect("div.post-content li a")
count = len(temp)
for i in range (0,count):
    city = root.cssselect("div.post-content li a")[i]
    cityname = city.text
    try:    
        citylink = city.get('href')
        meetup = scraperwiki.scrape(citylink)
        meetupRoot = lxml.html.fromstring(meetup)
    except:
        pass

    number = 0
    try: 
        members = meetupRoot.cssselect("ul.metaBox a")[0]
        str = members.text_content()
        number=filter(lambda x: x.isdigit(), str)
    except:
        pass

    data = {
        'cityname': cityname,
        'members': number
    }
    scraperwiki.sqlite.save(unique_keys=['cityname'], data=data)
    i=i+1

import scraperwiki
import lxml.html


# Blank Python
# work in progress

html = scraperwiki.scrape("http://hackshackers.com/chapters/")
root = lxml.html.fromstring(html)
temp = root.cssselect("div.post-content li a")
count = len(temp)
for i in range (0,count):
    city = root.cssselect("div.post-content li a")[i]
    cityname = city.text
    try:    
        citylink = city.get('href')
        meetup = scraperwiki.scrape(citylink)
        meetupRoot = lxml.html.fromstring(meetup)
    except:
        pass

    number = 0
    try: 
        members = meetupRoot.cssselect("ul.metaBox a")[0]
        str = members.text_content()
        number=filter(lambda x: x.isdigit(), str)
    except:
        pass

    data = {
        'cityname': cityname,
        'members': number
    }
    scraperwiki.sqlite.save(unique_keys=['cityname'], data=data)
    i=i+1

