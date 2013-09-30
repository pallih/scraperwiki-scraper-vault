import scraperwiki

scraperwiki.sqlite.attach("scrapercursus defence")

position = int(scraperwiki.sqlite.get_var("position", 1))

links = scraperwiki.sqlite.select("id, URL from 'scrapercursus defence'.swdata where id >= %d order by id" % position)

for link in links:
    url = link["URL"]

    html = scraperwiki.scrape(url)
    data = {"URL":url, "HTML": html}
    scraperwiki.sqlite.save(["URL"], data}
    scraperwiki.sqlite.save_var("position", link["id"])

#Handig jongen, zo'n tellertje erbij. Zie daarvoor positionimport scraperwiki

scraperwiki.sqlite.attach("scrapercursus defence")

position = int(scraperwiki.sqlite.get_var("position", 1))

links = scraperwiki.sqlite.select("id, URL from 'scrapercursus defence'.swdata where id >= %d order by id" % position)

for link in links:
    url = link["URL"]

    html = scraperwiki.scrape(url)
    data = {"URL":url, "HTML": html}
    scraperwiki.sqlite.save(["URL"], data}
    scraperwiki.sqlite.save_var("position", link["id"])

#Handig jongen, zo'n tellertje erbij. Zie daarvoor position