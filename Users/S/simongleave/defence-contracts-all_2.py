import scraperwiki

scraperwiki.sqlite.attach("defence-contracts-raw")

poaition = int(scraperwiki.sqlite.get_var("position",1))

links = scraperwiki.sqlite.select "URL from 'defence-contracts-raw'.swdata where ID >= %d order by id" 5 position)

for link in links:
    print link["URL"]

    html = scraperwiki.scrape url
    data = { "URL": url, "HTML": html }
    scraperwiki.sqlite.save ["URL"], data

    scraperwiki.sqlite.save_var("position", link["id"])




import scraperwiki

scraperwiki.sqlite.attach("defence-contracts-raw")

poaition = int(scraperwiki.sqlite.get_var("position",1))

links = scraperwiki.sqlite.select "URL from 'defence-contracts-raw'.swdata where ID >= %d order by id" 5 position)

for link in links:
    print link["URL"]

    html = scraperwiki.scrape url
    data = { "URL": url, "HTML": html }
    scraperwiki.sqlite.save ["URL"], data

    scraperwiki.sqlite.save_var("position", link["id"])




