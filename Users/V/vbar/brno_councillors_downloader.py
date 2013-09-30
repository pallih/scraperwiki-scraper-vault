import scraperwiki

url = "http://www.brno.cz/sprava-mesta/volene-organy-mesta/zastupitelstvo-mesta-brna/clenove-zastupitelstva-mesta-brna/"
html = scraperwiki.scrape(url)
data = { 'url': url, 'html': html }
scraperwiki.sqlite.save(unique_keys=['url'], data=data)
import scraperwiki

url = "http://www.brno.cz/sprava-mesta/volene-organy-mesta/zastupitelstvo-mesta-brna/clenove-zastupitelstva-mesta-brna/"
html = scraperwiki.scrape(url)
data = { 'url': url, 'html': html }
scraperwiki.sqlite.save(unique_keys=['url'], data=data)
