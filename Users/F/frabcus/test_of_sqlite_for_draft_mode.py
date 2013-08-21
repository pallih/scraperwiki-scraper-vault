import scraperwiki

scraperwiki.sqlite.save(['hi'], {'hi': 'value-of-hi'})
print scraperwiki.sqlite.execute('select * from swdata')


