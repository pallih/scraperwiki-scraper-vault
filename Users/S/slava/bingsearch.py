import scraperwiki
import mechanize
import urllib, urllib2
import cookielib
import re
import httplib




#addresses = scraperwiki.scrape("http://dl.dropbox.com/u/14865435/bigcities.txt")
addresses = scraperwiki.scrape("http://dl.dropbox.com/u/14865435/morocco.txt")
class BingSearch:

    def __init__(self):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        self.opener.open("http://www.bing.com/maps/default.aspx")

    def patch_http_response_read(func):
        def inner(*args):
            try:
                return func(*args)
            except httplib.IncompleteRead, e:
                return e.partial
    
        return inner
    httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

    def query(self, address):
        url = "http://www.bing.com/maps/default.aspx?"+urllib.urlencode({'q':address})+"&form=MPSRCH"
        headers=[
            ('X-MicrosoftAjax', 'Delta=true'),
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'),
            ('Referer', 'http://www.bing.com/maps/')]
        
        params = {
            "scriptManager":"scriptManager|go",
            "__EVENTTARGET":"",
            "__EVENTARGUMENT":"",
            "__VIEWSTATE":"",
            "q":address,
            "qs":"n",
            "form":"FDNF",
            "qf":"",
            "qfwh":"",
            "TaskHost$CollectionsViewer_state":"false",
            "TaskHost$Search_state":"false",
            "TaskHost$TaskDescription":"",
            "MapControl$MapControl":"{'TR':{'Latitude':51.768107924832485,'Longitude':69.00001525800002}, 'BL':{'Latitude':41.82077787552165,'Longitude':-11.332015991999981},'BO':0,'BA':false,'B':0,'MS':0,'Z':4,'MW':914,'MH':166,'C':{'Latitude':33.589017,'Longitude':-7.545993} }",
            "zoomLevelFromSearch":"",
            "centerPointFromSearch":"",
            "taskbarSearchIdField":"310249380",
            "Search_FDQuery":address,
            "Search_FDASData":"",
            "goa":"",
            "mapViewChangedSinceLastExplicitSearch":"",
            "jsondata":"",
            "mapApps":"",
            "go":"" }

        self.opener.addheaders = headers
        r = self.opener.open(url, urllib.urlencode(params))
        content = r.read()
        match = re.findall(r'<span.*?"searchPageLatLongContent".*?>(.+?)</span', content, re.U|re.I)
        if match!=[] and match[0].strip() != '':
            result = match[0].split(" ")
        else: 
            result = ('','')
        return result




id=1
#scraperwiki.sqlite.execute("delete from data")

bs = BingSearch()
for row in addresses.split("\n"):
    row=row.strip()

    if row == '': continue

    row=row.split("|")
    row[1] = row[1].strip()

    if row[1] == '': continue
    #print row

    #addr = row[1] + ', ' + row[2] + ', ' + row[3]
    addr = row[0]+ ', ' + row[1]

    #if addr.find("Ang. ") != 0:
        #r = re.findall(r'Ang\.(.+?) Et.', row[1], re.U | re.I)
    #    row[1] = re.sub(r', Quartier .+?$', '', row[1])
    #    row[1] = re.sub(r' Citee .+?$', '', row[1])
    #    row[1] = re.sub(r' - .+?$', '', row[1])
    #    print addr
    #    ll=bs.query(addr)
    #else:
    #    print "SKIP - ", addr
    #    ll=('','')
    print addr
    ll=bs.query(addr)
    #scraperwiki.sqlite.save(unique_keys=['id'], data={'id':id, 'bfcid': row[0], 'address': row[1], 'lat':ll[0], 'lng':ll[1], 'city':row[2]}, table_name='data')
    scraperwiki.sqlite.save(unique_keys=['id'], data={'id':id, 'lat':ll[0], 'lng':ll[1], 'city':row[0]}, table_name='cities_data')
    id+=1
    
    
import scraperwiki
import mechanize
import urllib, urllib2
import cookielib
import re
import httplib




#addresses = scraperwiki.scrape("http://dl.dropbox.com/u/14865435/bigcities.txt")
addresses = scraperwiki.scrape("http://dl.dropbox.com/u/14865435/morocco.txt")
class BingSearch:

    def __init__(self):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        self.opener.open("http://www.bing.com/maps/default.aspx")

    def patch_http_response_read(func):
        def inner(*args):
            try:
                return func(*args)
            except httplib.IncompleteRead, e:
                return e.partial
    
        return inner
    httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

    def query(self, address):
        url = "http://www.bing.com/maps/default.aspx?"+urllib.urlencode({'q':address})+"&form=MPSRCH"
        headers=[
            ('X-MicrosoftAjax', 'Delta=true'),
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'),
            ('Referer', 'http://www.bing.com/maps/')]
        
        params = {
            "scriptManager":"scriptManager|go",
            "__EVENTTARGET":"",
            "__EVENTARGUMENT":"",
            "__VIEWSTATE":"",
            "q":address,
            "qs":"n",
            "form":"FDNF",
            "qf":"",
            "qfwh":"",
            "TaskHost$CollectionsViewer_state":"false",
            "TaskHost$Search_state":"false",
            "TaskHost$TaskDescription":"",
            "MapControl$MapControl":"{'TR':{'Latitude':51.768107924832485,'Longitude':69.00001525800002}, 'BL':{'Latitude':41.82077787552165,'Longitude':-11.332015991999981},'BO':0,'BA':false,'B':0,'MS':0,'Z':4,'MW':914,'MH':166,'C':{'Latitude':33.589017,'Longitude':-7.545993} }",
            "zoomLevelFromSearch":"",
            "centerPointFromSearch":"",
            "taskbarSearchIdField":"310249380",
            "Search_FDQuery":address,
            "Search_FDASData":"",
            "goa":"",
            "mapViewChangedSinceLastExplicitSearch":"",
            "jsondata":"",
            "mapApps":"",
            "go":"" }

        self.opener.addheaders = headers
        r = self.opener.open(url, urllib.urlencode(params))
        content = r.read()
        match = re.findall(r'<span.*?"searchPageLatLongContent".*?>(.+?)</span', content, re.U|re.I)
        if match!=[] and match[0].strip() != '':
            result = match[0].split(" ")
        else: 
            result = ('','')
        return result




id=1
#scraperwiki.sqlite.execute("delete from data")

bs = BingSearch()
for row in addresses.split("\n"):
    row=row.strip()

    if row == '': continue

    row=row.split("|")
    row[1] = row[1].strip()

    if row[1] == '': continue
    #print row

    #addr = row[1] + ', ' + row[2] + ', ' + row[3]
    addr = row[0]+ ', ' + row[1]

    #if addr.find("Ang. ") != 0:
        #r = re.findall(r'Ang\.(.+?) Et.', row[1], re.U | re.I)
    #    row[1] = re.sub(r', Quartier .+?$', '', row[1])
    #    row[1] = re.sub(r' Citee .+?$', '', row[1])
    #    row[1] = re.sub(r' - .+?$', '', row[1])
    #    print addr
    #    ll=bs.query(addr)
    #else:
    #    print "SKIP - ", addr
    #    ll=('','')
    print addr
    ll=bs.query(addr)
    #scraperwiki.sqlite.save(unique_keys=['id'], data={'id':id, 'bfcid': row[0], 'address': row[1], 'lat':ll[0], 'lng':ll[1], 'city':row[2]}, table_name='data')
    scraperwiki.sqlite.save(unique_keys=['id'], data={'id':id, 'lat':ll[0], 'lng':ll[1], 'city':row[0]}, table_name='cities_data')
    id+=1
    
    
