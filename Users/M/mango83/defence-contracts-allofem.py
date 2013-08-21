import scraperwiki

scraperwiki.sqlite.attach("ministry_of_defence_things")

position = int(scraperwiki.sqlite.get_var("position", 1))

links = scraperwiki.sqlite.select("id, URL from 'ministry_of_defence_things'.swdata where id>= %d order by id" % position)

for link in links:
    url = link["URL"]


    html = scraperwiki.scrape(url)
    data = { "URL": url, "HTML": html } 
    scraperwiki.sqlite.save(["URL"], data)

    scraperwiki.sqlite.save_var("position", link["id"])




