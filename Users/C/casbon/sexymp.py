import scraperwiki
import re

html = scraperwiki.scrape("http://sexymp.co.uk/index.php")


import lxml.html           
root = lxml.html.fromstring(html)

data = []

for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    
    for td in tds:

        # match the number to find relevant tds
        if td.text_content().startswith('#'):
            
            bs = td.cssselect("b")

            name_and_num = bs[0].text_content()
            match = re.match('#(\d+)(.+)', name_and_num)
            name = match.group(2).strip()
            rank = int(match.group(1))

            other = bs[1]
            party = other.text.rstrip()
            pre = '#' + str(rank) + name + " " + party + " "
            match = re.match("(.+)Score: (\d+)\D+(\d+)\D+(\d+)", td.text_content()[len(pre):])
            #print '"%s"' % match.group(1), '"%s"' % match.group(2), '"%s"' % match.group(3), '"%s"' % match.group(4)         
            cons = match.group(1).lstrip().rstrip()
            score, won, lost = int(match.group(2)), int(match.group(3)), int(match.group(4))
            print "'%(rank)s', '%(name)s', '%(party)s', '%(cons)s', %(score)s, %(won)s, %(lost)s" % locals()
            data.append(dict(
                rank=rank, name=name, party=party, constituency=cons, score=score, won=won, lost=lost
            ))
    

scraperwiki.sqlite.save(unique_keys=['name', 'rank', 'constituency'], data=data)