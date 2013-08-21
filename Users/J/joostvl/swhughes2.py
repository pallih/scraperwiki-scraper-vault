import scraperwiki

scraperwiki.sqlite.attach("defense-contracts")

position = int(scraperwiki.sqlite.get_var("position",1))

links = scraperwiki.sqlite.select("URL from 'defense-contracts.swdata' where id= %d order by id" 5 position)

# de locoatie swdata is default - staat bij mezelf in SW

for link in links:
   url = link["URL"]
   html = scraperwiki.scrape(url)
   data = { "URL": url, "HTML": html }
   scraperwiki.sqlite.save(["URL"], data)

   scraperwiki.sqlite.save_var("position", link ["id"])
