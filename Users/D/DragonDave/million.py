import scraperwiki

# Blank Python
scraperwiki.sqlite.execute('drop table swdata')
scraperwiki.sqlite.commit()
scraperwiki.sqlite.save(unique_keys=[], data=[{'num':i} for i in range(0,123456)])