import scraperwiki

# Blank Python

baseurl = "http://ptv.vic.gov.au/getting-around/stations-and-stops/metropolitan-trains/"

html = scraperwiki.scrape(baseurl)

import lxml.html
root = lxml.html.fromstring(html)
root_anchors = root.cssselect("ul[class='clearfix '] li a")

row = {}
for root_a in root_anchors:
    suburb = root_a.text
    sub_html = scraperwiki.scrape(root_a.attrib['href'])

    sub_root = lxml.html.fromstring(sub_html)
    sub_anchors = sub_root.cssselect("ul[class='clearfix'] li a")

    for sub_a in sub_anchors:
        station = sub_a.text
        stat_html = scraperwiki.scrape(sub_a.attrib['href'])
        
        stat_root = lxml.html.fromstring(stat_html)
        stat_anchors = stat_root.cssselect("a[target='_blank']")
    
        latlong = filter(lambda x: 'maps.google.com' in x.attrib['href'], stat_anchors)[0].attrib['href']
        row['suburb'] = suburb
        row['station'] = station
        row['latlong'] = latlong
        
        scraperwiki.sqlite.save(table_name='station_latlong', unique_keys=['station'], data=row)


        

import scraperwiki

# Blank Python

baseurl = "http://ptv.vic.gov.au/getting-around/stations-and-stops/metropolitan-trains/"

html = scraperwiki.scrape(baseurl)

import lxml.html
root = lxml.html.fromstring(html)
root_anchors = root.cssselect("ul[class='clearfix '] li a")

row = {}
for root_a in root_anchors:
    suburb = root_a.text
    sub_html = scraperwiki.scrape(root_a.attrib['href'])

    sub_root = lxml.html.fromstring(sub_html)
    sub_anchors = sub_root.cssselect("ul[class='clearfix'] li a")

    for sub_a in sub_anchors:
        station = sub_a.text
        stat_html = scraperwiki.scrape(sub_a.attrib['href'])
        
        stat_root = lxml.html.fromstring(stat_html)
        stat_anchors = stat_root.cssselect("a[target='_blank']")
    
        latlong = filter(lambda x: 'maps.google.com' in x.attrib['href'], stat_anchors)[0].attrib['href']
        row['suburb'] = suburb
        row['station'] = station
        row['latlong'] = latlong
        
        scraperwiki.sqlite.save(table_name='station_latlong', unique_keys=['station'], data=row)


        

