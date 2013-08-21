import scraperwiki

# Blank Python
import scraperwiki
params = {
      'City' : 'bluffton',
    'County' : '07',
    'Facility_Type' : '206',
    'button' : 'Search',
    'button_search' : '1'
    }
html = scraperwiki.scrape("http://www.scdhec.gov/environment/envhealth/food/htm/inspection-rating.asp#results?City=bluffton&County=07&Facility_Name=&Facility_Type=206&button=Search&button_search=1", params)
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    rows = tr.cssselect("td")
    data = {
      'date' : rows[4].text_content(),
      'facility name' : rows[0].text_content(), 
      'street' : rows[1].text_content(), 
      'city' : rows[2].text_content(), 
      'score' : rows[3].text_content()    
    }
    scraperwiki.sqlite.save(unique_keys=["facility name","date"], data=data)

