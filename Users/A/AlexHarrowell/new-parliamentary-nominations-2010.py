import scraperwiki
import BeautifulSoup
from scraperwiki import datastore
import re
    
# limit the range scanned to avoid overloading the system
iconstart, iconlast = 50, 250


def TWFYconstituencies():
    constituencylisturl = "http://www.theyworkforyou.com/boundaries/new-constituencies.tsv"
    constituencylist = scraperwiki.scrape(constituencylisturl)
    result = { }
    for con, r in re.findall("(.*?)\t(.*?)\n", constituencylist):
        lcon = re.sub(",", "", con)
        lcon = re.sub("-", " ", lcon).lower()
        lcon = " ".join(sorted(lcon.split()))
        result[lcon] = con
    return result

twfyconstituencies = TWFYconstituencies()

corrections = { "hull east":"kingston upon hull east", "hull north":"kingston upon hull north", "hull west":"kingston upon hull west", 
                "hull west and hessle":"kingston upon hull west and hessle" }
def RegularizeConstituency(scon):
    lcon = re.sub(",", "", scon)
    lcon = re.sub("-", " ", lcon)
    lcon = re.sub("  ", " ", lcon)
    lcon = re.sub(" &amp; ", " and ", lcon)
    lcon = re.sub(" & ", " and ", lcon)
    lcon = lcon.lower()
    lcon = corrections.get(lcon, lcon)
    lcon = " ".join(sorted(lcon .split()))
    if lcon not in twfyconstituencies:
        print "Missing const", scon, lcon
        print twfyconstituencies.keys()
        print twfyconstituencies.values()
    return twfyconstituencies[lcon]  # will throw an exception if missing


html = scraperwiki.scrape('http://election.pressassociation.com/Nominations/general.php')
page = BeautifulSoup.BeautifulSoup(html)
constituencies = []

for p in page.findAll('p', {'class': 'constituency-heading'}):
    cons = p.string
    number, const = cons.split('.')
    constituencies.append(RegularizeConstituency(const.lstrip()))
length = str(len(constituencies))
print length + ' constituencies identified'

candidatelists = page.findAll('ul', {'class': 'nominations'})
print 'got candidate lists'
mapped = zip(constituencies, candidatelists)
uniquekey = ["constituency"]
counter = 0


for con, canlist in mapped[iconstart:iconlast]:
    conname = con
    
    for candidate in canlist.findAll('li'):
        counter += 1
        c = candidate.string
        n, a = c.split(' (')
        name = n.strip(' +*')
        affiliation = a.strip(' )')
        can = dict(constituency=con, name=name, affiliation=affiliation)
        print iconstart, can
        datastore.save(unique_keys=uniquekey, data=can)
        print 'data-row number ' + str(counter) + 'saved'
    iconstart += 1