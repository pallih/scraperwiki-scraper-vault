import scraperwiki

from bs4 import BeautifulSoup

import  datetime
now = datetime.datetime.now()


scraperwiki.sqlite.attach("rijkictdashboard")

scrapings = scraperwiki.sqlite.select("* from 'rijkictdashboard'.swdata")

n=1

for scraping in scrapings:
    url = "https://www.rijksictdashboard.nl" + scraping["URL"]
    dingetje = scraperwiki.scrape(url)
    soup = BeautifulSoup(dingetje)
    logje = str(now) + " " + str(n)
    titel = soup.find("h1", {"class": "title"}).get_text() 
    kosten = soup.find("div", {"class": "spending displayblock"}).get_text().replace("Meerjarige projectkosten", "").replace(",", ".").strip()
    minister = soup.find("span", {"class": "field-content"}).get_text()
    peildatum = soup.find("div", {"class": "peil_datum displayblock"}).get_text().replace("Peildatum", "").strip()
    status = soup.find("div", {"class": "projectstatus displayblock"}).get_text().replace("Projectstatus", "").strip()
    graaf = soup.find("div", {"class":"graph"})
    linkje= graaf.find("a")
    tstring = str(linkje)
    echtgoed = tstring.split('"')
    kurl = "https://www.rijksictdashboard.nl" + str(echtgoed[1])
    kostje = scraperwiki.scrape(kurl)
    soep = BeautifulSoup(kostje)
    tabelleke = soep.find("tbody")
    beterrr = tabelleke.find_all("td")
    eerstea = str(beterrr[4])
    leega = eerstea.split("div")
    totaala = leega[0] + leega[-1]
    bedraga = totaala.replace("<td>", "").replace("<> mln</td>", " mln").replace (",", ".")
    eersteb = str(beterrr[10])
    leegb = eersteb.split("div")
    totaalb = leegb[0] + leegb[-1]
    bedragb = totaalb.replace("<td>", "").replace("<> mln</td>", " mln").replace (",", ".")
    eerstec = str(beterrr[16])
    leegc = eerstec.split("div")
    totaalc = leegc[0] + leegc[-1]
    bedragc = totaalc.replace("<td>", "").replace("<> mln</td>", " mln").replace (",", ".")
    daga = str(beterrr[1]).replace("<td>", "").replace("</td>", "")
    dagb = str(beterrr[2]).replace("<td>", "").replace("</td>", "")
    dagc = str(beterrr[3]).replace("<td>", "").replace("</td>", "")
    data = {"status": status, "titel": titel, "kosten": kosten, "peildatum": peildatum, "id":logje, "startdatum": daga, "initeindd" : dagb, "acteindd": dagc, "bedragi": bedraga, "bedragac": bedragb, "bedragrea": bedragc, "minister": minister}
    scraperwiki.sqlite.save(["id"], data)
    n+=1


