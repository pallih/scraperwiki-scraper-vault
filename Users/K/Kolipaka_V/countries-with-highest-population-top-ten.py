import scraperwiki
from BeautifulSoup import BeautifulSoup

print "Counries with highest population-Top ten"


scraperwiki.metadata.save('data_columns', ['Country', '2010 Population', '2000 Population', 'population increase 2000-2010', 'Expected population for year 2050']) 

def scrape_ptable(Soup):
     data_ptable = Soup.find("table", { "class" : "sortable" })  
     data_ptable = Soup.find("table")
     data_ptable = Soup.find("thead")
     data_ptable = Soup.find("tbody")

     rows = data_ptable.findAll("tr")
     data_table = Soup.find("tbody")
     rows = data_ptable.findAll("tr")
    
     for row in rows:
          populationrecord = {}

          table_population = row.findAll("td")
          if table_population:
                populationrecord['Country'] = table_population[0].text
                populationrecord['2010 population'] = table_population[1].text
                populationrecord['2000 Population'] = table_population[2].text
                populationrecord['Population increase 2000-2010'] = table_population[3].text
                populationrecord['Expected population for year 2050'] = table_population[4].text
                print populationrecord,
                print "---------"
                scraperwiki.datastore.save(["Country"], populationrecord)

geturl=("http://www.internetworldstats.com/stats8.htm/")
BeautifulSoap=scraperwiki.scrape(geturl)
scrape_ptable(Soup)












        












            