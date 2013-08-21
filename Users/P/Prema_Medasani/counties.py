import scraperwiki
from BeautifulSoup import BeautifulSoup
html = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_counties_of_England_by_population_in_1971')
my_html = BeautifulSoup(html)
counties_table=my_html.find("table", { "class" : "wikitable" })
def my_scraper101(my_html):
    scraperwiki.metadata.save('data_columns', ['Rank', 'County', 'Total Population'])
    datas = counties_table.findAll("tr")
    for row in datas:         
        record = {}
        cells = row.findAll("td")
        if len(cells)>2:
            record['Rank'] = cells[0].text
            record['County'] = cells[1].text
            record['Total Population'] = cells[2].text
            print record

            scraperwiki.datastore.save(['Rank'], record)

my_scraper101(my_html)