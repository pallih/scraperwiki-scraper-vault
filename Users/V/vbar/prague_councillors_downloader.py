import scraperwiki

url = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/slozeni_zastupitelstva/index.html?size=100"
html = scraperwiki.scrape(url)
data = { 'url': url, 'html': html }
scraperwiki.sqlite.save(unique_keys=['url'], data=data)


