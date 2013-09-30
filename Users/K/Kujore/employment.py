import scraperwiki
from BeautifulSoup import BeautifulSoup
def employment(soup):
    scraperwiki.metadata.save('data_columns',['constituency','Region', 'Male','women', 'total','rate'])
    data_table = soup.find("table",{"class" : "in-article sortable"})
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['constituency'] = table_cells[0].text
            record['Region'] = table_cells[1].text
            record['Male'] = table_cells[2].text
            record['Women'] = table_cells[3].text
            record['total'] = table_cells[4].text
            record['rate'] = table_cells[5].text
            print record, "--------"
            scraperwiki.datastore.save(["constituency"], record)

website_url = ("http://www.guardian.co.uk/news/datablog/2010/nov/17/unemployment-and-employment-statistics-economics")
html = scraperwiki.scrape(website_url)
soup = Beautifulsoup(html)
employment(soup)import scraperwiki
from BeautifulSoup import BeautifulSoup
def employment(soup):
    scraperwiki.metadata.save('data_columns',['constituency','Region', 'Male','women', 'total','rate'])
    data_table = soup.find("table",{"class" : "in-article sortable"})
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['constituency'] = table_cells[0].text
            record['Region'] = table_cells[1].text
            record['Male'] = table_cells[2].text
            record['Women'] = table_cells[3].text
            record['total'] = table_cells[4].text
            record['rate'] = table_cells[5].text
            print record, "--------"
            scraperwiki.datastore.save(["constituency"], record)

website_url = ("http://www.guardian.co.uk/news/datablog/2010/nov/17/unemployment-and-employment-statistics-economics")
html = scraperwiki.scrape(website_url)
soup = Beautifulsoup(html)
employment(soup)