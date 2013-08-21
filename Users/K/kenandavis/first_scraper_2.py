from scraperwiki import scrape
from scraperwiki.sqlite import save

data = {
    'firstname':'Thomas',
    'lastname':'Levine'
}

print data

save([], data)

