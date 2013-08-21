import scraperwiki

# Blank Python
print "This is a <em>fragment</em> of HTML."
import scraperwiki
html = scraperwiki.scrape("http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Administrative_Divisions/Number_of_States.aspx")
print html
#import lxml.html
#root = lxml.html.fromstring(html)
#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        print data
#scraperwiki.sqlite.save(unique_keys=['country'], data=data)
#select * from data order by years_in_school desc limit 10

