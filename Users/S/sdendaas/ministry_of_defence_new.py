import scraperwiki

position = int(scraperwiki.sqlite.get_var("position", 1))

scraperwiki.sqlite.attach("defence-contracts-raw")

links = scraperwiki.sqlite.select("id, URL from 'defence-contracts-raw'.swdata where id>= %d order by id" % position)

for link in links:
    url = link["URL"]

    html = scraperwiki.scrape(url)
    data = { "URL": url, "HTML": html }
    scraperwiki.sqlite.save(["URL"], data)

    scraperwiki.sqlite.set_var("position", link["id"])