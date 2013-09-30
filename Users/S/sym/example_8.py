import scraperwiki

# Blank Python

text = scraperwiki.scrape('http://www.lipsum.com/')
for word in text.split(' '):
    if word.lower().startswith('l'):
        print wordimport scraperwiki

# Blank Python

text = scraperwiki.scrape('http://www.lipsum.com/')
for word in text.split(' '):
    if word.lower().startswith('l'):
        print word