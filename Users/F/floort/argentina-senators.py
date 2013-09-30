import scraperwiki
from BeautifulSoup import BeautifulSoup

SERVER = "http://www.senado.gov.ar"
INDEX_PATH = "/web/senadores/senadores.php"
# This page lists all the "Senadores"
page = BeautifulSoup(scraperwiki.scrape(SERVER+INDEX_PATH))
# Find the tabel with all the senators
# Search by border color because of all the nested tables without id's or classes.
table = page.find("table", {"bordercolor":"#ece8e1"})
# Each row contains a senator
for row in table.findAll("tr")[1:]: # The first row is the header. Skip it.
    td = row.findAll("td")
    scraperwiki.datastore.save(["name",], {
        "name": td[1].text,
        # Replace height=50 with height=100 to get larger imgs      vvvvvvvvvvv
        "picture": SERVER+"/web/senadores/"+td[0].find("img")["src"][:-2]+"100",
        "district": td[2].text,
        "party": td[3].text,
    })import scraperwiki
from BeautifulSoup import BeautifulSoup

SERVER = "http://www.senado.gov.ar"
INDEX_PATH = "/web/senadores/senadores.php"
# This page lists all the "Senadores"
page = BeautifulSoup(scraperwiki.scrape(SERVER+INDEX_PATH))
# Find the tabel with all the senators
# Search by border color because of all the nested tables without id's or classes.
table = page.find("table", {"bordercolor":"#ece8e1"})
# Each row contains a senator
for row in table.findAll("tr")[1:]: # The first row is the header. Skip it.
    td = row.findAll("td")
    scraperwiki.datastore.save(["name",], {
        "name": td[1].text,
        # Replace height=50 with height=100 to get larger imgs      vvvvvvvvvvv
        "picture": SERVER+"/web/senadores/"+td[0].find("img")["src"][:-2]+"100",
        "district": td[2].text,
        "party": td[3].text,
    })