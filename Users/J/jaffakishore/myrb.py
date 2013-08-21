from pprint import pformat
import requests
import lxml.html
import scraperwiki
import urllib
import time

session = requests.session()

start = 0
base_url = 'http://classifieds.myredbook.com/classified.php?%s'
while True:
    if start < 480:
        payload = 'ORDER BY adeditdate desc&offset=%s&poffset=0' % start
        payload = { 'sqlquery' : 'WHERE 1=1', 'sqlquery2' : "*", 'sqlquery3' : payload} 
    if start >= 480:
        payload = 'ORDER BY adeditdate desc&offset=%s&poffset=0' % str(start-480)
        payload = { 'sqlquery' : 'WHERE subcatid=10 AND icon5=1', 'sqlquery2=&sqlquery3' : payload}
        if start >= 960:
            start = -30
    payload = urllib.urlencode(payload)
    url = base_url % payload
    #print url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0',
        'Referer': 'http://classifieds.myredbook.com/classified.php?sqlquery=WHERE+subcatid%3D10+AND+icon5%3D1&sqlquery2%3D%26sqlquery3=ORDER+BY+adeditdate+desc%26offset%3D0%26poffset%3D999'
    }
    r = session.get(url, headers=headers)
    root = lxml.html.fromstring(r.text)
    print "Scraping Page : "+str((start/30)+1)
    #root = lxml.html.parse(url).getroot()
    #print lxml.etree.tostring(root)
    profiles = root.cssselect('.class2 table')[2].cssselect('div')
    urls = root.cssselect('.class2 table')[2].cssselect('td.classcat3')   

    if len(profiles) == 0:
        print "No Ads found!"
        raise SystemExit
    #print "Ads found !"
    i = 1
    for index in range(1, len(profiles), 2):
        try:
            profile = profiles[index]
            urlindex = (index - 1)/2
            #print lxml.etree.tostring(urls[urlindex])
            allAttributes = profile.getprevious().cssselect('a')[0].items()
            tempCity = lxml.etree.tostring(profile)
            startCity = tempCity.find("City:")+6
            endCity = tempCity.lower().find("<br/>", startCity)
            if endCity == -1:
                endCity = tempCity.lower().find("<br>", startCity)
    
            tempName = lxml.etree.tostring(profile)
            startName = tempName.find("Name:")+6
            endName = tempName.lower().find("<br/>", startName)
            if endName == -1:
                endName = tempName.lower().find("<br>", startName)
            tempPhone = tempName[startName:endName].strip().title()
            startPhone = tempPhone.rfind(":")+1
            endPhone = len(tempPhone)
            
            tempTime = lxml.etree.tostring(profile)
            startTime = tempTime.find("</b>")+4
            tempTime = lxml.etree.tostring(profile)
            endTime = tempTime.lower().find("am", startTime)+2
            if endTime == -1:
                endTime = tempTime.lower().find("pm", startTime)+2    
            if endTime == -1:
                endTime = tempTime.lower().find("<br>", startTime)  
            if endTime == -1:
                endTime = tempTime.lower().find("<br/>", startTime)
            if endTime == -1:
                endTime = tempTime.lower().find("<a", startTime) 
            
            adUsername = profile.cssselect('b')[0].text
            adURL = 'http://classifieds.myredbook.com%s' % allAttributes[0][1]
            adThumbnail = lxml.etree.tostring(urls[urlindex].cssselect('img')[0])
            adID = adURL.replace("http://classifieds.myredbook.com/classified.php?adid=", "")
            adTitle = profile.getprevious().cssselect('a')[0].text
            adCity = tempCity[startCity:endCity].strip().title()
            adPhone = tempPhone[startPhone:endPhone].strip().title()
            adTime = tempTime[startTime:endTime].lower().replace("on", "").strip().title()    
            #continue
            
            #if index < 6:
            #    print "%s) %s - %s (%s)" % (adID, adUsername, adTitle, adPhone)
            #print str(index)+" "+str(adID)
            data = {'id': adID, 'username': adUsername, 'title': adTitle, 'phone' : adPhone, 'city' : adCity, 'time' : adTime, 'thumbnail' : adThumbnail,}
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        except:
            continue
            print "profile skipped !"
    start = start + 30
    #print "sleeping"
    time.sleep(10)
    #print start
    #print "%s profiles scraped" % len(profiles)