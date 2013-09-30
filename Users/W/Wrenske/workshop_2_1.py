import scraperwiki

position = int(scraperwiki.sqlite.get_var("position", 1))

scraperwiki.sqlite.attach("datajournalistiekworkshop_nicola_hughes_probeersel")

links = scraperwiki.sqlite.select("id, URL from 'datajournalistiekworkshop_nicola_hughes_probeersel'.swdata where id>= %d order by id" % position)

for link in links:
    url = link["URL"]
#gaat naar dictionary, call it by its key
  
    html = scraperwiki.scrape(url)
    data = { "URL": url, "HTML": html }
#kan van alles genoemd worden, data is gewoon een keuze hier
    scraperwiki.sqlite.save(["URL"], data)
#data in originele scraper zijn nog niet compleet geïmporteerd!

import scraperwiki

position = int(scraperwiki.sqlite.get_var("position", 1))

scraperwiki.sqlite.attach("datajournalistiekworkshop_nicola_hughes_probeersel")

links = scraperwiki.sqlite.select("id, URL from 'datajournalistiekworkshop_nicola_hughes_probeersel'.swdata where id>= %d order by id" % position)

for link in links:
    url = link["URL"]
#gaat naar dictionary, call it by its key
  
    html = scraperwiki.scrape(url)
    data = { "URL": url, "HTML": html }
#kan van alles genoemd worden, data is gewoon een keuze hier
    scraperwiki.sqlite.save(["URL"], data)
#data in originele scraper zijn nog niet compleet geïmporteerd!

