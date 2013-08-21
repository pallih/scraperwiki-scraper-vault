# Blank Python
import scraperwiki           
html = scraperwiki.scrape("http://menmedia.co.uk/manchestereveningnews/news/crime/s/1409643_greater_manchester_crime_rates_rocket_by_13_per_cent_in_a_single_month")
print html
import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[align='left'] tableizer.table"):
    tds = tr.cssselect("td")
    data = {
      'neighbourhood' : tds[0].text_content(),
      'crime/ASB Jan 2011' : int(tds[4].text_content())
    }
    scraperwiki.sqlite.save(unique_keys=['neighbourhood'], data=data)           
