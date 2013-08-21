import scraperwiki

scraperwiki-sqlite.attach("defence-contracts-raw")

position = int(scraperwiki.sqlite.get_var 'position', 1)

links = sraperwiki.sqlite.select("URL from 'defence-contracts-raw'.swdata" where id>= %d order by id" % position)

for link in links:
    url = link("URL")

    html = scraperwiki.scrap(url)
    data = { "URL: url, "HTML": html }
    scraperwiki.sqlite.save(["URL"],data)
    scraperwiki.sqlite.save_var ("position", link["id"]



    






