
# Scraper for Premier League, Bundesliga, and Seria A league tables between 2009-2012

# Extra countries can be added (france) or Divisions (england2, germany2 etc.) in countries list

# Ant Wilson 2013

import scraperwiki
import lxml.html

countries = ['england', 'germany', 'italy']

class EOS_Table(object):
    """class representing the league table at the end of the season"""
    
    fields = ["Position"       ,
              "Team"           , 
              "Matches played" ,
              "Matches won"    ,
              "Draws"          ,
              "Matches lost"   ,
              "Goals For"      ,
              "Goals Against"  ,
              "Goal Difference",
              "Points"         ,
              "League"         ,
              "Year"           ]
    
    def is_ascii(self,s):
        return all(ord(c) < 128 for c in s)

    # when initialised, entity will parse for selectors and save resulting dict
    def __init__(self, element, year, league):

        row = element.cssselect("tr")

        for el in row:
            td = el.cssselect("td")

            store = {}

            if (self.is_ascii(td[0].text_content())):
                for i in range(0,10):
                    store[self.fields[i]] = td[i].text_content().strip()

                store[self.fields[10]] = league
                store[self.fields[11]] = year
                store['Key'] = store['Team'] + '-' + str(store['Year'])

                scraperwiki.sqlite.save(unique_keys=["Key"], data=store)

# main. Grabs league table for each combination of country-year. Leagues/Countries set at top of file.
for country in countries:
    for year in range(2009,2013):
        html = scraperwiki.scrape("http://www.soccerstats.com/latest.asp?league=%s_%s" % (country, year))
        root = lxml.html.fromstring(html)

        for element in root.cssselect("table.stat"):                
            EOS_Table(element, year, country)
