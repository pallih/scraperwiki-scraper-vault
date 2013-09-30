import scraperwiki

scraperwiki.sqlite.attach("contracts_ministry_of_defence")

links = scraperwiki.sqlite.select("URL from 'contracts_ministry_of_defence'.swdata")

for link in links:
    url =  link ["URL"]

    html = scraperwiki.scrape(url)
    data = { "URL": url, "HTML":html }
    scraperwiki.sqlite.save(["URL"]), data

    
import scraperwiki

scraperwiki.sqlite.attach("contracts_ministry_of_defence")

links = scraperwiki.sqlite.select("URL from 'contracts_ministry_of_defence'.swdata")

for link in links:
    url =  link ["URL"]

    html = scraperwiki.scrape(url)
    data = { "URL": url, "HTML":html }
    scraperwiki.sqlite.save(["URL"]), data

    
