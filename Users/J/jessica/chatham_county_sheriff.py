import scraperwiki

# Blank Python
import scraperwiki

html = scraperwiki.scrape("http://chathamsheriff.org/Corrections/Bookings24hrs.aspx")
print html
import lxml.html           
root = lxml.html.fromstring(html)
for table in root.cssselect("div[id='gallery'] table"):
    tds = table.cssselect("td")
    data = {
      'picture' : tds[0].cssselect("img")[0].get("src"),
      'name' : tds[1].text_content(), 
      'birth date' : tds[2].text_content(),
      'race' : tds[3].text_content(),
      'arrest date' : tds[4].text_content(),
      'agency' : tds[7].text_content(),
      'bond' : tds[8].text_content(),
      'charge' : tds[9].text_content()
    }
    
    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

.encode('ascii').replace('Â', 'x')


