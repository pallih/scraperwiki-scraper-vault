import scraperwiki

# URL to pull the data from
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/contraceptive.htm")

#print html

#import the HTML string 
 
import lxml.html

root = lxml.html.fromstring(html)

for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_of_survey' : tds[2].text_content(),
      'age_range' : tds[5].text_content(),
      'any_method_percent' : tds[6].text_content(),
      'modern_methods_percent' : tds[8].text_content()

    }
    print data


    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
