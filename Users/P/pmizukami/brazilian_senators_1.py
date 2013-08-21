import scraperwiki
from BeautifulSoup import BeautifulSoup

INDEX_PAGE = "http://www.senado.gov.br/senadores/"

page = BeautifulSoup(scraperwiki.scrape(INDEX_PAGE))
table = page.find("table", {"id":"senadores"}).find("tbody")
for row in table.findAll("tr"):
    scraperwiki.sqlite.save(["name", ], {
        "name": row.find("td", {"class":"colNomeSenador"}).text,
        "party": row.find("td", {"class":"colPartido"}).text,
        "province": row.find("td", {"class":"colUF"}).text.strip("&nbsp;"),
        "phone": row.find("td", {"class":"colTelsSenador"}).text,
        "fax": row.find("td", {"class":"colFaxSenador"}).text,
        "email": row.find("td", {"class":"colEmaisSenador"}).find("a")["href"][7:],
    })