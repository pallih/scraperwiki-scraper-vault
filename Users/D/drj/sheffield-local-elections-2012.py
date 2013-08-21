import scraperwiki
import urllib2

url="https://www.sheffield.gov.uk/your-city-council/elections/election-results/2012/"

print urllib2.urlopen(url).read()