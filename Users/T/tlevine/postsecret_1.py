import scraperwiki

SOURCESCRAPER = 'postsecret'

scraperwiki.sqlite.attach(SOURCESCRAPER)
card=scraperwiki.sqlite.select('url1,url2,sunday from postcards ORDER BY random() LIMIT 1')[0]


print("""
<h1>Random PostSecret</h1>
<h3>from %s</h3>
<img src="%s" alt="">
""" % (card['sunday'],card['url1']))

if card['url2']!=None:
  print("""<img src="%s" alt="">""" % (card['url2']))