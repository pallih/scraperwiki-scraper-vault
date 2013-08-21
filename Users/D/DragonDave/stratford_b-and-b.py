import scraperwiki
import urllib, lxml.html,string
transbase=string.maketrans("/ &().'", "-_-----")

baseurl='http://discover-stratford.com/bed-and-breakfast.cfm'
basedata=urllib.urlopen(baseurl).read()

root = lxml.html.fromstring(basedata)
places=[]
for place in root.cssselect("div[class='acc_content'] a"):
    coords=None
    url='http://discover-stratford.com/'+place.get('href')
    placedata=urllib.urlopen(url).read()
    placeroot=lxml.html.fromstring(placedata)
    for boxout in placeroot.cssselect("div[class='detail-main-heading']"):
        if boxout.cssselect("h2")[0].text_content()=="Location":
            for li in boxout.getnext().cssselect('li'):
                attemptpostcode=scraperwiki.geo.extract_gb_postcode(li.text_content())
                if attemptpostcode: coords=scraperwiki.geo.gb_postcode_to_latlng(attemptpostcode)
        if boxout.cssselect("h2")[0].text_content()=="Amenities & Facilities":
            features=map(str.strip,boxout.tail.split(','))
    # title, features, coords are our gold.
    
    data={}
    for i in features:
        if i=='': continue
        data[i.translate(transbase)]=True
    data['title']=placeroot.cssselect("title")[0].text_content().partition('-')[2]
    try:
        data['xcoord']=coords[0]
        data['ycoord']=coords[1]
    except TypeError:
        pass
    data['url']=place.get('href')
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)
    
    

                
