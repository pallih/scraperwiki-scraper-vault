import scraperwiki

from bs4 import BeautifulSoup

proberen = scraperwiki.scrape('https://www.rijksictdashboard.nl/content/project/biometrie-de-vreemdelingenketen-bvk/kosten_doorlooptijd/23876')
print proberen

soep = BeautifulSoup(proberen)

tabelleke = soep.find("tbody")


beterrr = tabelleke.find_all("td")






eerste = str(beterrr[4])

leeg = eerste.split("div")

totaal = leeg[0] + leeg[-1]

bedrag = totaal.replace("<td>", "").replace("<> mln</td>", " mln")

print beterrr




# Blank Python

import scraperwiki

from bs4 import BeautifulSoup

proberen = scraperwiki.scrape('https://www.rijksictdashboard.nl/content/project/biometrie-de-vreemdelingenketen-bvk/kosten_doorlooptijd/23876')
print proberen

soep = BeautifulSoup(proberen)

tabelleke = soep.find("tbody")


beterrr = tabelleke.find_all("td")






eerste = str(beterrr[4])

leeg = eerste.split("div")

totaal = leeg[0] + leeg[-1]

bedrag = totaal.replace("<td>", "").replace("<> mln</td>", " mln")

print beterrr




# Blank Python

