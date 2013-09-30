import scraperwiki

scraperwiki.sqlite.attach("trialanderror")

links = scraperwiki.sqlite.select("URL from 'trialanderror'.swdata")

for link in links:
    url =  link ["URL"]

    html = scraperwiki.scrape(url) 
    data = { "URL": url, "HTML": html }
    scraperwiki.sqlite.save(["URL"], data)

import scraperwiki

scraperwiki.sqlite.attach("trialanderror")

links = scraperwiki.sqlite.select("URL from 'trialanderror'.swdata")

for link in links:
    url =  link ["URL"]

    html = scraperwiki.scrape(url) 
    data = { "URL": url, "HTML": html }
    scraperwiki.sqlite.save(["URL"], data)

