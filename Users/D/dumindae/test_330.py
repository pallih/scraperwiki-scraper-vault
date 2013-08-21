import scraperwiki
import dateutil.parser 
from geopy import geocoders  
import urlparse
import lxml.html

def extractEventsInCatogary( url, catogary):
   
    html = scraperwiki.scrape(url)



    root = lxml.html.fromstring(html)
    for div in root.cssselect("div[class='top_events'] div[class='left_block']"):
         eventURL = "http://www.event.lk" + div.cssselect("div[class='img_thumb_text'] a")[0].attrib['href']
         name = div.cssselect("div[class='img_thumb_text'] a")[0].text_content()
         monthSpans = div.cssselect("div[class='img_thumb_text'] p[class='img_thumb_subhead'] span[class='month']")    
         if len(monthSpans )==2:
             fromMonth = div.cssselect("div[class='img_thumb_text'] p[class='img_thumb_subhead'] span[class='month']")[0].text_content()
             fromDay = div.cssselect("div[class='img_thumb_text'] p[class='img_thumb_subhead'] span[class='day']")[0].text_content()
             endMonth = div.cssselect("div[class='img_thumb_text'] p[class='img_thumb_subhead'] span[class='month']")[1].text_content()
             endDay = div.cssselect("div[class='img_thumb_text'] p[class='img_thumb_subhead'] span[class='day']")[1].text_content()
             fromDateStr = fromDay.split(',')[0] + " " + fromMonth + " " + fromDay.split(',')[1]
             fromDate = dateutil.parser.parse(fromDateStr[0:12])
             endDateStr = endDay.split(',')[0] + " " + endMonth + " " + endDay.split(',')[1]
             endDate = dateutil.parser.parse(endDateStr[0:12])
         else:
             fromMonth = div.cssselect("div[class='img_thumb_text'] p[class='img_thumb_subhead'] span[class='month']")[0].text_content()
             fromDay = div.cssselect("div[class='img_thumb_text'] p[class='img_thumb_subhead'] span[class='day']")[0].text_content()
             fromDateStr = fromDay.split(',')[1] + " " + fromMonth + " " + fromDay.split(',')[0]
             fromDate = dateutil.parser.parse(fromDateStr)
             endDate = fromDate
         building =  div.cssselect("div[class='img_thumb_text'] p[class='img_thumb_subhead'] span[class='vn'] a")[0].text_content()
         placeLink = div.cssselect("div[class='img_thumb_text'] p[class='img_thumb_subhead'] span[class='vn'] a")[0].attrib['href']
         placeHTML = scraperwiki.scrape("http://www.event.lk" + placeLink)
         placeNode = lxml.html.fromstring(placeHTML)
         place = building  
         for addressElement in placeNode.cssselect("div[class='venue_address'] b"):
               place = place  +  "," + addressElement.text_content()
         geoLocationURLs =  placeNode.cssselect("div[class='venue_address'] div iframe")
         geoLocationURL = 'NA'
         longitude = -1
         lattitude = -1
         if len(geoLocationURLs) > 0:
            geoLocationURL = geoLocationURLs[0].attrib['src']
            parsed = urlparse.urlparse(geoLocationURL)
            llValue = urlparse.parse_qs(parsed.query)['ll']
            longitude = llValue[0].split(',')[0]   
            lattitude = llValue[0].split(',')[1]
         eventPageHTML = scraperwiki.scrape(eventURL)
         eventPage= lxml.html.fromstring(eventPageHTML )
         eventImageURL = "http://www.event.lk" + eventPage.cssselect("div[class='event_body'] img")[0].attrib['src']
         print "Event details"
         print "catogary : " + catogary
         print "event : " + name
         print "start date : " + str(fromDate)
         print "end date : " + str(endDate)
         print "place : " + place
         print "url : " + eventURL
         print "imageURL: " +  eventImageURL
         print "longitude : " + str(longitude)
         print "lattitude : " + str(lattitude)
         print "-----------------------------"
         data = {
          'catogary' : catogary,  
          'name' : name,
          'fromDate' : fromDate,
          'toDate' : endDate,
          'place' : place,
          'url' : eventURL,
          'imageURL' :  eventImageURL,  
          'longitude' :  longitude,
          'lattitude' :  lattitude
         }  
 

         scraperwiki.sqlite.save(unique_keys=['catogary','name','fromDate','toDate'], data=data)


mainRootHtml = scraperwiki.scrape("http://www.event.lk/event/index/category/1")
mainRoot = lxml.html.fromstring(mainRootHtml)

for catogary in mainRoot.cssselect("li[class='exhibition']"):
    catURL =  "http://www.event.lk" + catogary .cssselect("a")[0].attrib['href']
    catogary = catogary.cssselect("a")[0].text_content()
    extractEventsInCatogary(catURL,catogary)
    html = scraperwiki.scrape(catURL)
    root = lxml.html.fromstring(html)
    pages = root.cssselect("div[id='page_link'] a") 
    if len(pages) > 0 :
        for page in pages :
           pageUrl = "http://www.event.lk" + page.attrib['href']
           extractEventsInCatogary(pageUrl,catogary)    
   
 
    



    




