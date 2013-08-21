"""
Compares scrapers, looking for common code.
"""


import scraperwiki
import json
import re


def stripped_python(s):
    for l in s.split("\n"):
        l = l.strip()
        if l != "":
            yield l


def rolling_hash(s,window_length=6):
    hashes = [hash(0)]*window_length
    current_hash = 0
    modulus = 2**30
    multiplier = 41 # it's prime, y'know
    remove = (multiplier**window_length)%modulus
    i = 0
    for x in s:
        h = hash(x)
        current_hash = (multiplier*current_hash + hash(x) - remove*hashes[0])%modulus
        hashes = hashes[1:] + [h]
        i += 1
        if i >= window_length:
            yield current_hash


class Relation():
    def __init__(self):
        self.d = {}
    def relate(self,k,v):
        if k not in self.d:
            self.d[k] = set()
        self.d[k].add(v)
    def pairs_by_keys_in_common(self):
        p = {}
        c = 0
        for (k,v) in self.d.iteritems():
            c += 1
            l = sorted(v)
            for i in range(len(l)):
                x = l[i]
                for j in range(i+1,len(l)):
                    y = l[j]
                    p[(x,y)] = 1 + p.get((x,y),0)
            if c%250 == 0:
                print "examined %d hash values"%c
        return p



def main():
    decoder = json.JSONDecoder()

    # 1000000 is a stupidly large number?
    scrapers = decoder.decode(scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/scraper/search?format=jsondict&maxrows=1000000"))
    # would be nicer if there was an "offset" to avoid generating superhuge JSON objects
    # even nicer if we could do it incrementally

    r = Relation()

    for d in scrapers:
        short_name = d["short_name"]
        if short_name[-8:] == ".emailer":
            continue
        print short_name
        details = decoder.decode(scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name=%s&version=-1&quietfields=runevents%%7Cdatasummary%%7Cuserroles%%7Chistory"%short_name))[0]
        code = details["code"]

        # search code for mentions views
        v = re.compile("views\\.scraperwiki\\.com/run/([A-Za-z0-9_]*)")
        for other in re.findall(v,code):
            scraperwiki.sqlite.save(unique_keys=["from","to","type"],data={"from":short_name, "to":other, "type":"mention"})

        # prepare table of hashes to find common code        
        for h in rolling_hash(stripped_python(code)):
            r.relate(h,short_name)

        # find attachments
        for other in details["attachables"]:
            scraperwiki.sqlite.save(unique_keys=["from","to","type"],data={"from":short_name, "to":other, "type":"attachment"})

    # now find the common code
    for ((x,y),n) in r.pairs_by_keys_in_common().iteritems():
        scraperwiki.sqlite.save(unique_keys=["from","to","type"],data={"from":x, "to":y, "type":"common code", "strength":n})


main()


