import scraperwiki
from bs4 import BeautifulSoup
import time
# Blank Python

stem = 'http://www.start.umd.edu/gtd/search/Results.aspx?page=1&casualties_type=&casualties_max=&country=4&expanded=no&charttype=line&chart=regions&ob=GTDID&od=desc#results-table'

def main():
    startUrl = 'http://www.start.umd.edu/gtd/search/BrowseBy.aspx?category=country'
    response = scraperwiki.scrape(startUrl)
    soup = BeautifulSoup(response)
    results = soup.findAll('td')
    for result in results:
        result = result.find('a')
        result =  result.get('href')[13:]
        newUrl = 'http://www.start.umd.edu/gtd/search/Results.aspx?page=%s&casualties_type=&casualties_max=&%s&expanded=no&charttype=line&chart=regions&ob=GTDID&od=desc#results-table' % (1,result)
        getTable(newUrl)
        time.sleep(2)

def getTable(newUrl):
    response = scraperwiki.scrape(newUrl)
    soup2 = BeautifulSoup(response)
    table_results = soup2.find('table', attrs = {'class':'results'})
    table_results = table_results.find('tbody')
    table_results = table_results.findAll('tr')
    for tr in table_results:
        output = tr.findAll('td')
        dr = {}
        dr['GTD_ID'] = output[0].getText()
        dr['Date'] = output[1].getText()
        dr['Country'] = output[2].getText()
        dr['City'] = output[3].getText()
        dr['Perpetrators'] = output[4].getText()
        dr['Fatalities'] = output[5].getText()
        dr['Injured'] = output[6].getText()
        dr['TargetType'] = output[7].getText()
        scraperwiki.sqlite.save(unique_keys=['GTD_ID'],data=dr)

main()
import scraperwiki
from bs4 import BeautifulSoup
import time
# Blank Python

stem = 'http://www.start.umd.edu/gtd/search/Results.aspx?page=1&casualties_type=&casualties_max=&country=4&expanded=no&charttype=line&chart=regions&ob=GTDID&od=desc#results-table'

def main():
    startUrl = 'http://www.start.umd.edu/gtd/search/BrowseBy.aspx?category=country'
    response = scraperwiki.scrape(startUrl)
    soup = BeautifulSoup(response)
    results = soup.findAll('td')
    for result in results:
        result = result.find('a')
        result =  result.get('href')[13:]
        newUrl = 'http://www.start.umd.edu/gtd/search/Results.aspx?page=%s&casualties_type=&casualties_max=&%s&expanded=no&charttype=line&chart=regions&ob=GTDID&od=desc#results-table' % (1,result)
        getTable(newUrl)
        time.sleep(2)

def getTable(newUrl):
    response = scraperwiki.scrape(newUrl)
    soup2 = BeautifulSoup(response)
    table_results = soup2.find('table', attrs = {'class':'results'})
    table_results = table_results.find('tbody')
    table_results = table_results.findAll('tr')
    for tr in table_results:
        output = tr.findAll('td')
        dr = {}
        dr['GTD_ID'] = output[0].getText()
        dr['Date'] = output[1].getText()
        dr['Country'] = output[2].getText()
        dr['City'] = output[3].getText()
        dr['Perpetrators'] = output[4].getText()
        dr['Fatalities'] = output[5].getText()
        dr['Injured'] = output[6].getText()
        dr['TargetType'] = output[7].getText()
        scraperwiki.sqlite.save(unique_keys=['GTD_ID'],data=dr)

main()
