import scraperwiki
#import re
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['RacePosition', 'Driver', 'Team', 'QualiPosition'])

# scrape_table function: gets passed an individual page (single race) to scrape​
def scrape_table(scrapeurl,racename):
    scrapehtml = scraperwiki.scrape(scrapeurl)
    scrapesoup = BeautifulSoup(scrapehtml)
    data_table = scrapesoup.find("table", { "class" : "raceResults" })
    if data_table:
        rows = data_table.findAll("tr")
        for row in rows:
            # Set up our data record - we'll need it later
            record = {}
            table_cells = row.findAll("td")
            if table_cells: 
                record['RaceYear'] = season
                record['Race'] = racename
                record['RacePosition'] = table_cells[0].text
                record['CarNumber'] = table_cells[1].text
                record['Driver'] = table_cells[2].text
                record['Team'] = table_cells[3].text
                record['Laps'] = table_cells[4].text
                record['TimeReason'] = table_cells[5].text
                record['QualiPosition'] = table_cells[6].text
                record['Points'] = table_cells[7].text
                # Save the record to the datastore
                scraperwiki.datastore.save(["RaceYear", "Race", "Driver"], record)
        
# scrape_and_look_for_next_link function: trawls through each season to find the GPs
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    yearresults = soup.find("table", { "class" : "raceResults" })
    gps = yearresults.findAll("tr")
    for gp in gps:
        gpresults = gp.findAll("td")
        if gpresults: 
            next_url = base_url + str(gpresults[0].a['href'])
            racename = gpresults[0].text
            scrape_table(next_url,racename)

# ---------------------------------------------------------------------------
# START HERE
# ---------------------------------------------------------------------------
base_url = 'http://www.formula1.com'
# Change the second digit below to scavenge more years.​​  61 covers up to 2010.
for season in range(0,61):
    season = season + 1950
    starting_url = base_url + '/results/season/%s/' % (season)
    scrape_and_look_for_next_link(starting_url)
import scraperwiki
#import re
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['RacePosition', 'Driver', 'Team', 'QualiPosition'])

# scrape_table function: gets passed an individual page (single race) to scrape​
def scrape_table(scrapeurl,racename):
    scrapehtml = scraperwiki.scrape(scrapeurl)
    scrapesoup = BeautifulSoup(scrapehtml)
    data_table = scrapesoup.find("table", { "class" : "raceResults" })
    if data_table:
        rows = data_table.findAll("tr")
        for row in rows:
            # Set up our data record - we'll need it later
            record = {}
            table_cells = row.findAll("td")
            if table_cells: 
                record['RaceYear'] = season
                record['Race'] = racename
                record['RacePosition'] = table_cells[0].text
                record['CarNumber'] = table_cells[1].text
                record['Driver'] = table_cells[2].text
                record['Team'] = table_cells[3].text
                record['Laps'] = table_cells[4].text
                record['TimeReason'] = table_cells[5].text
                record['QualiPosition'] = table_cells[6].text
                record['Points'] = table_cells[7].text
                # Save the record to the datastore
                scraperwiki.datastore.save(["RaceYear", "Race", "Driver"], record)
        
# scrape_and_look_for_next_link function: trawls through each season to find the GPs
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    yearresults = soup.find("table", { "class" : "raceResults" })
    gps = yearresults.findAll("tr")
    for gp in gps:
        gpresults = gp.findAll("td")
        if gpresults: 
            next_url = base_url + str(gpresults[0].a['href'])
            racename = gpresults[0].text
            scrape_table(next_url,racename)

# ---------------------------------------------------------------------------
# START HERE
# ---------------------------------------------------------------------------
base_url = 'http://www.formula1.com'
# Change the second digit below to scavenge more years.​​  61 covers up to 2010.
for season in range(0,61):
    season = season + 1950
    starting_url = base_url + '/results/season/%s/' % (season)
    scrape_and_look_for_next_link(starting_url)
