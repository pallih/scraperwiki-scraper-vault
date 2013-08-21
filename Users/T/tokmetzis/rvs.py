import scraperwiki
from lxml import html
from urlparse import urljoin

site = "http://www.raadvanstate.nl/uitspraken/zoeken_in_uitspraken/default.asp?page=&pageSize=10&start=0&order_by=verdict_publication_date&order=DESC&verdict_rightsarea_1=all&verdict_rightsarea_2=&verdict_rightsarea_3=&verdict_procedure=all&datum_vanaf_dag=&datum_vanaf_maand=&datum_vanaf_jaar=&datum_tot_dag=&datum_tot_maand=&datum_tot_jaar=&zoeken_veld=uitspraak&verdict_choise=alles"
page = scraperwiki.scrape(site)
page = html.fromstring(page)

# dus als je op de table komt, en als je onclick tegenkomt, haal je op wat er achter staat

for uitspraak in page.cssselect("table"):
    table = uitspraak.get("onclick")
    if table == None: continue
    table = table[22:-2]
    url = urljoin(site, table)
    page = scraperwiki.scrape(site)
    page = html.fromstring(page)
    div#PrintKlaar table table
    print page


                                          





for article in page.cssselect("article.artikel"):
    link = article.cssselect("footer a")[0].get("href")
    article_page = html.fromstring(scraperwiki.scrape(link))
    title = article_page.cssselect("article.artikel h1")[0].text_content()
    text = article_page.cssselect ("article.artikel p") [0].text_content()
    data = {"url": link, "title": title, "text": text}
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)





# Ik wil naar de zoekpagina van de RvS gaan: http://www.raadvanstate.nl/uitspraken/zoeken_in_uitspraken/default.asp
# Daar wil ik in het zoekveld de term uitspraak intypen en dan op zoek drukken
# Vervolgens wil ik met de gevonden treffers openenen en sorteren:
# Sorteren kan van tevoren via het verfijnmenu, of in de documenten zelf. 
# Ik wil in ieder geval weten in welke Kamer de zaak is behandeld (RO, Vreemdelingen, Algemene), of het Hoger Beroep is, EV of MV, Voorlopige voorziening, voorlopige voorziening hoofdzaak, Herziening en Wraking.
# Ik wil ook weten wat voor soort zaak het is, inhoudelijk: Onder RO: Bestemmingsplannen (per provincie), Geluid, Luchtvaart, Natuurbescherming, Ontgrondingen, Schadevergoedingen, Trace en wegverbredingen, Wet dwangsom en beroep, overige. 
# 
# die info wil ik gestructureerd naar binnen halen