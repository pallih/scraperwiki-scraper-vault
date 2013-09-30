import scraperwiki
import lxml.html

def fetch_html(url):
    try:
        html = scraperwiki.scrape(url)
        return lxml.html.fromstring(html)
    except:
        try:
            html = scraperwiki.scrape(url)
            return lxml.html.fromstring(html)
        except:
            pass
        print "Failed to fetch url: " + url
    return 
    

print "Starting!"

try:
    scraperwiki.sqlite.execute("drop table agencies")
except:
    pass

scraperwiki.sqlite.execute("create table agencies (title string, link string, address string, phonenumber string, lng int, lat int, postcode string)")

def extract(result):
    res = {}
    title = link = address = phonenumber = lng = lat = postcode = ''
    res['title'] = result.find_class('notranslate')[0].xpath('a')[0].text.strip()
    res['link'] = "http://www.google.ca/?travel%20agencies#sclient=psy-ab&hl=en&site=&source=hp&q=travel+agencies+in+canada&pbx=1&oq=travel+agencies+in+canada&aq=f&aqi=g3g-v1&aql=1&gs_sm=e&gs_upl=3413l5999l0l6040l25l16l0l0l0l0l280l3350l0.3.12l15l0&bav=on.2,or.r_gc.r_pw.,cf.osb&fp=7e50e7fb95e9d6e1&biw=1680&bih=965" + result.find_class('notranslate')[0].xpath('a')[0].attrib['href']
    res['address'] = result.xpath('div/ul/li')[0].text
    res['phonenumber'] = result.xpath('div/ul/li')[1].text
    res['postcode'] = scraperwiki.geo.extract_gb_postcode(res['address'])
    
    loc = scraperwiki.geo.gb_postcode_to_latlng(res['postcode'])
    if loc:
        res['lng'], res['lat'] = loc[0], loc[1]
    else:
        res['lng'], res['lat'] = "",""

    return res

for page_num in range(1, 788):

    url = "http://www.google.ca/?travel%20agencies#sclient=psy-ab&hl=en&site=&source=hp&q=travel+agencies+in+canada&pbx=1&oq=travel+agencies+in+canada&aq=f&aqi=g3g-v1&aql=1&gs_sm=e&gs_upl=3413l5999l0l6040l25l16l0l0l0l0l280l3350l0.3.12l15l0&bav=on.2,or.r_gc.r_pw.,cf.osb&fp=7e50e7fb95e9d6e1&biw=1680&bih=965
    #url  = "http://www.google.ca/?travel%20agencies#sclient=psy-ab&hl=en&site=&source=hp&q=travel+agencies+in+canada&pbx=1&oq=travel+agencies+in+canada&aq=f&aqi=g3g-v1&aql=1&gs_sm=e&gs_upl=3413l5999l0l6040l25l16l0l0l0l0l280l3350l0.3.12l15l0&bav=on.2,or.r_gc.r_pw.,cf.osb&fp=7e50e7fb95e9d6e1&biw=1680&bih=965"
    
    root = fetch_html(url)
    if root:
        try:
            for result in root.find_class('organisation-wrapper'):
                details = extract(result)
                scraperwiki.sqlite.execute('insert into dentists values (?, ?, ?, ?, ?, ?, ?)', (
                                details['title'], 
                                details['link'], 
                                details['address'], 
                                details['phonenumber'], 
                                details['lng'], 
                                details['lat'], 
                                details['postcode']))

                scraperwiki.sqlite.commit()
        except:
            print "Failed on: %s --> " % (url, details['title'])
    


import scraperwiki
import lxml.html

def fetch_html(url):
    try:
        html = scraperwiki.scrape(url)
        return lxml.html.fromstring(html)
    except:
        try:
            html = scraperwiki.scrape(url)
            return lxml.html.fromstring(html)
        except:
            pass
        print "Failed to fetch url: " + url
    return 
    

print "Starting!"

try:
    scraperwiki.sqlite.execute("drop table agencies")
except:
    pass

scraperwiki.sqlite.execute("create table agencies (title string, link string, address string, phonenumber string, lng int, lat int, postcode string)")

def extract(result):
    res = {}
    title = link = address = phonenumber = lng = lat = postcode = ''
    res['title'] = result.find_class('notranslate')[0].xpath('a')[0].text.strip()
    res['link'] = "http://www.google.ca/?travel%20agencies#sclient=psy-ab&hl=en&site=&source=hp&q=travel+agencies+in+canada&pbx=1&oq=travel+agencies+in+canada&aq=f&aqi=g3g-v1&aql=1&gs_sm=e&gs_upl=3413l5999l0l6040l25l16l0l0l0l0l280l3350l0.3.12l15l0&bav=on.2,or.r_gc.r_pw.,cf.osb&fp=7e50e7fb95e9d6e1&biw=1680&bih=965" + result.find_class('notranslate')[0].xpath('a')[0].attrib['href']
    res['address'] = result.xpath('div/ul/li')[0].text
    res['phonenumber'] = result.xpath('div/ul/li')[1].text
    res['postcode'] = scraperwiki.geo.extract_gb_postcode(res['address'])
    
    loc = scraperwiki.geo.gb_postcode_to_latlng(res['postcode'])
    if loc:
        res['lng'], res['lat'] = loc[0], loc[1]
    else:
        res['lng'], res['lat'] = "",""

    return res

for page_num in range(1, 788):

    url = "http://www.google.ca/?travel%20agencies#sclient=psy-ab&hl=en&site=&source=hp&q=travel+agencies+in+canada&pbx=1&oq=travel+agencies+in+canada&aq=f&aqi=g3g-v1&aql=1&gs_sm=e&gs_upl=3413l5999l0l6040l25l16l0l0l0l0l280l3350l0.3.12l15l0&bav=on.2,or.r_gc.r_pw.,cf.osb&fp=7e50e7fb95e9d6e1&biw=1680&bih=965
    #url  = "http://www.google.ca/?travel%20agencies#sclient=psy-ab&hl=en&site=&source=hp&q=travel+agencies+in+canada&pbx=1&oq=travel+agencies+in+canada&aq=f&aqi=g3g-v1&aql=1&gs_sm=e&gs_upl=3413l5999l0l6040l25l16l0l0l0l0l280l3350l0.3.12l15l0&bav=on.2,or.r_gc.r_pw.,cf.osb&fp=7e50e7fb95e9d6e1&biw=1680&bih=965"
    
    root = fetch_html(url)
    if root:
        try:
            for result in root.find_class('organisation-wrapper'):
                details = extract(result)
                scraperwiki.sqlite.execute('insert into dentists values (?, ?, ?, ?, ?, ?, ?)', (
                                details['title'], 
                                details['link'], 
                                details['address'], 
                                details['phonenumber'], 
                                details['lng'], 
                                details['lat'], 
                                details['postcode']))

                scraperwiki.sqlite.commit()
        except:
            print "Failed on: %s --> " % (url, details['title'])
    


