import scraperwiki
from bs4 import BeautifulSoup as Soup
from urllib import urlopen

# This scrapes http://www.police.uk/data/, pulling in the percentage of
# crimes that led to court outcomes for each force.

soup = Soup(urlopen('http://www.police.uk/data/').read())

scraperwiki.sqlite.save(
    unique_keys=[],
    data=dict([
        (td.parent.td.text.replace('&', 'and'), int(td.text))
        for td in soup('td') if td.has_key('class') and td['class'] == ['rate']
    ])
)import scraperwiki
from bs4 import BeautifulSoup as Soup
from urllib import urlopen

# This scrapes http://www.police.uk/data/, pulling in the percentage of
# crimes that led to court outcomes for each force.

soup = Soup(urlopen('http://www.police.uk/data/').read())

scraperwiki.sqlite.save(
    unique_keys=[],
    data=dict([
        (td.parent.td.text.replace('&', 'and'), int(td.text))
        for td in soup('td') if td.has_key('class') and td['class'] == ['rate']
    ])
)