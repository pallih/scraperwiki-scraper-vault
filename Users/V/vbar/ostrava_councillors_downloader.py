import scraperwiki

url = "http://www.ostrava.cz/cs/urad/mesto-a-jeho-organy/zastupitelstvo-mesta/slozeni-zastupitelstva-1/clenove-zastupitelstva-mesta"
html = scraperwiki.scrape(url)
data = { 'url': url, 'html': html }
scraperwiki.sqlite.save(unique_keys=['url'], data=data)

import scraperwiki

url = "http://www.ostrava.cz/cs/urad/mesto-a-jeho-organy/zastupitelstvo-mesta/slozeni-zastupitelstva-1/clenove-zastupitelstva-mesta"
html = scraperwiki.scrape(url)
data = { 'url': url, 'html': html }
scraperwiki.sqlite.save(unique_keys=['url'], data=data)

