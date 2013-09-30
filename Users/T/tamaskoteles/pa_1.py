import scraperwiki
import lxml.html
import re

# Parse the main page
def parse_main(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("div[id='Hinnat'] tr"):
        parse_row(tr.cssselect("td"))

# Parse a data row
def parse_row(tds):
    if len(tds)==5: 
        anchors = tds[0].cssselect("a")
        if len(anchors) > 0:
            
            id_match = re.search(r'\d+', anchors[0].get('href'))
            if id_match:
                station = tds[0].text_content()
                p95 = tds[2].text_content()
                p98 = tds[3].text_content()
                pD = tds[4].text_content()
                
                # Get data from database
                data = {'id' : id_match.group(), 'station' : station}
                changed = True
                try:
                    data_list = scraperwiki.sqlite.select("* from swdata where id = " + id_match.group())
                    if data_list:
                        data = data_list[0]
                        changed = False
                except scraperwiki.sqlite.SqliteError, e:
                    print str(e)
                    
                if (not 'lat' in data) and (not 'lon' in data):
                    parse_map(data)
                    changed = True
        
                if (not 'e95' in data) or (not data['e95'] == p95):
                    data['e95'] = p95
                    changed = True
                if (not 'e98' in data) or (not data['e98'] == p98):
                    data['e98'] = p98
                    changed = True
                if (not 'diesel' in data) or (not data['diesel'] == pD):
                    data['diesel'] = pD
                    changed = True
                    
                
                if changed:
                    print "Saving updated"
                    print data
                    scraperwiki.sqlite.save(unique_keys=['id'], data=data)


# Parse map
def parse_map(data):
    url = "http://polttoaine.net/index.php?cmd=map&id=" + data['id']
    html = scraperwiki.scrape(url)
    latlon_match = re.search(r'(\d{2}\.\d+), (\d{2}\.\d+)', html)
    if latlon_match:
        data['lat'] = latlon_match.group(1)
        data['lon'] = latlon_match.group(2)

# Main
parse_main("http://polttoaine.net/index.php?cmd=kaikki")

# Haversine spherical distance calc NB not in use and not checked
"""def distance(lat1, lon1, lat2, lon2):
    radius = 6371 # radius of the Earth in km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d """
    import scraperwiki
import lxml.html
import re

# Parse the main page
def parse_main(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("div[id='Hinnat'] tr"):
        parse_row(tr.cssselect("td"))

# Parse a data row
def parse_row(tds):
    if len(tds)==5: 
        anchors = tds[0].cssselect("a")
        if len(anchors) > 0:
            
            id_match = re.search(r'\d+', anchors[0].get('href'))
            if id_match:
                station = tds[0].text_content()
                p95 = tds[2].text_content()
                p98 = tds[3].text_content()
                pD = tds[4].text_content()
                
                # Get data from database
                data = {'id' : id_match.group(), 'station' : station}
                changed = True
                try:
                    data_list = scraperwiki.sqlite.select("* from swdata where id = " + id_match.group())
                    if data_list:
                        data = data_list[0]
                        changed = False
                except scraperwiki.sqlite.SqliteError, e:
                    print str(e)
                    
                if (not 'lat' in data) and (not 'lon' in data):
                    parse_map(data)
                    changed = True
        
                if (not 'e95' in data) or (not data['e95'] == p95):
                    data['e95'] = p95
                    changed = True
                if (not 'e98' in data) or (not data['e98'] == p98):
                    data['e98'] = p98
                    changed = True
                if (not 'diesel' in data) or (not data['diesel'] == pD):
                    data['diesel'] = pD
                    changed = True
                    
                
                if changed:
                    print "Saving updated"
                    print data
                    scraperwiki.sqlite.save(unique_keys=['id'], data=data)


# Parse map
def parse_map(data):
    url = "http://polttoaine.net/index.php?cmd=map&id=" + data['id']
    html = scraperwiki.scrape(url)
    latlon_match = re.search(r'(\d{2}\.\d+), (\d{2}\.\d+)', html)
    if latlon_match:
        data['lat'] = latlon_match.group(1)
        data['lon'] = latlon_match.group(2)

# Main
parse_main("http://polttoaine.net/index.php?cmd=kaikki")

# Haversine spherical distance calc NB not in use and not checked
"""def distance(lat1, lon1, lat2, lon2):
    radius = 6371 # radius of the Earth in km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d """
    