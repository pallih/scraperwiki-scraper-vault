import scraperwiki
import lxml.html

url="http://www.weatherforecastmap.com"
url1=url+"/india/"
html=scraperwiki.scrape(url1)

print html

