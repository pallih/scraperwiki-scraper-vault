import scraperwiki
import lxml.html
import string
from datetime import datetime


activeURLList = ['http://m.atlantagasprices.com/StationProfile.aspx?s=KcsoMWNWyeY%3d&a=D1tN0EiGBVXzctfJbH3O9w%3d%3d',
                          'http://m.atlantagasprices.com/StationProfile.aspx?s=xEBLeJ6Vnrw%3d&a=D1tN0EiGBVXzctfJbH3O9w%3d%3d',
                          'http://m.atlantagasprices.com/StationProfile.aspx?s=uw5Wb8Ii2Jo%3d&a=D1tN0EiGBVXzctfJbH3O9w%3d%3d',
                          'http://m.atlantagasprices.com/StationProfile.aspx?s=A4Q5vk2GupM%3d&a=D1tN0EiGBVXzctfJbH3O9w%3d%3d']  
##
def getPageData():
  count = 0
  requestedData = []
  for url in activeURLList:
   page=scraperwiki.scrape(url)
   requestedData.append(lxml.html.fromstring(page))    
  return requestedData

##
def parseData(gasStation):
  soup = gasStation
  bodies = soup.cssselect('tbody')
  body = bodies[0]    
  rows = body.cssselect('tr')
  links = rows[0].cssselect('a')
  price = links[1].text_content()
  time = links[2].text_content()
  station = soup.cssselect('dt')
  station = station[0].text_content()
  today = datetime.today()
  data = {'date':today,'station':station,'price':price,'time':time}
  return data

##
prices = []
gasStations = getPageData()
for station in gasStations:
 prices.append(parseData(station))
 scraperwiki.sqlite.save(unique_keys=['date'], data=prices)

