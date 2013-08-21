import scraperwiki

# Blank Python

print 'Hello world'
html = scraperwiki.scrape("http://blog.zephod.com/")
print html

scraperwiki.sqlite.save([],{'site_content':html})
