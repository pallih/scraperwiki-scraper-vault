import scraperwiki

# Blank Python

scraperwiki.sqlite.save(table_name='space test', data={'1':'2'}, unique_keys=['1'])
scraperwiki.sqlite.save(table_name='space test', data={'1':'3', 'space test':'1'}, unique_keys=[])
print scraperwiki.sqlite.select('* from `space test`')

scraperwiki.sqlite.save(table_name='dotslash.',data={'1':'2'}, unique_keys=[])

scraperwiki.sqlite.execute ('create table if not exists [Pack my box with five dozen liquor jugs.] (hand gloves)')
scraperwiki.sqlite.execute ('create table if not exists [Packmyboxwithfivedozenliquorjugs.] (hand gloves)')
scraperwiki.sqlite.execute ('create table if not exists [The xylophone orchestra vowed to imbibe jugs of kumquat fizz.] (xylophone orchestra)')

scraperwiki.sqlite.commit()import scraperwiki

# Blank Python

scraperwiki.sqlite.save(table_name='space test', data={'1':'2'}, unique_keys=['1'])
scraperwiki.sqlite.save(table_name='space test', data={'1':'3', 'space test':'1'}, unique_keys=[])
print scraperwiki.sqlite.select('* from `space test`')

scraperwiki.sqlite.save(table_name='dotslash.',data={'1':'2'}, unique_keys=[])

scraperwiki.sqlite.execute ('create table if not exists [Pack my box with five dozen liquor jugs.] (hand gloves)')
scraperwiki.sqlite.execute ('create table if not exists [Packmyboxwithfivedozenliquorjugs.] (hand gloves)')
scraperwiki.sqlite.execute ('create table if not exists [The xylophone orchestra vowed to imbibe jugs of kumquat fizz.] (xylophone orchestra)')

scraperwiki.sqlite.commit()