import scraperwiki

# Blank Python

html = scraperwiki.scrape("http://www.atpworldtour.com/Matchfacts/Matchfacts-List.aspx?c=2&s=0&y=2012")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("tbody tr"):
    datum = tr.cssselect("td")
    data = {
        'Rank': datum[0].int(text_content()),
        'Player': datum[1].str(text_content()),
        'BP won': datum[2].int(text_content()),
        'BP played': datum[3].int(text_content()),
        'Percent won': datum[4].int(text_content()),
        'Matches played': datum[5].int(text_content()),
    }
    scraperwiki.sqlite.save(unique_keys=['Player'], data=data)
    print dataimport scraperwiki

# Blank Python

html = scraperwiki.scrape("http://www.atpworldtour.com/Matchfacts/Matchfacts-List.aspx?c=2&s=0&y=2012")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("tbody tr"):
    datum = tr.cssselect("td")
    data = {
        'Rank': datum[0].int(text_content()),
        'Player': datum[1].str(text_content()),
        'BP won': datum[2].int(text_content()),
        'BP played': datum[3].int(text_content()),
        'Percent won': datum[4].int(text_content()),
        'Matches played': datum[5].int(text_content()),
    }
    scraperwiki.sqlite.save(unique_keys=['Player'], data=data)
    print data