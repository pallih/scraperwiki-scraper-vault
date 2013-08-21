import scraperwiki

# URL to pull the data from
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/hum-sets.htm")

#print html

#import the HTML string 
 
import lxml.html

try:
    scraperwiki.sqlite.execute("drop table swdata")
except:
    pass



scraperwiki.sqlite.execute("CREATE TABLE 'swdata' (`country` text, `2010_population_distribution_percent_urban` text, `2010_population_distribution_percent_rural` text, `2010-2015_rate_of_population_change_percent_urban` text,`2010-2015_rate_of_population_change_percent_rural` text)")



root = lxml.html.fromstring(html)

for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      '2010_population_distribution_percent_urban' : tds[1].text_content(),
      '2010_population_distribution_percent_rural' : tds[3].text_content(),
      '2010-2015_rate_of_population_change_percent_urban' : tds[6].text_content(),
      '2010-2015_rate_of_population_change_percent_rural' : tds[8].text_content()

        
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)

   # scraperwiki.sqlite.execute('insert into human_settlements values (?, ?, ?, ?, ?)', (country, 2010_population_distribution_percent_urban, 2010_population_distribution_percent_rural, 2010-2015_rate_of_population_change_percent_urban, 2010-2015_rate_of_population_change_percent_rural))
    #        scraperwiki.sqlite.commit()


