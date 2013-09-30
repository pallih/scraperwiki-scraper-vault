import scraperwiki
import datetime
import lxml.html

debug = 0

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `colours` (`colour` text, `row_created` text)')
if debug:
    scraperwiki.sqlite.execute('DELETE FROM colours')
scraperwiki.sqlite.commit()

colours_in_db = scraperwiki.sqlite.select('* from colours')

if len(colours_in_db):
    # there are colours in the database - use them!
    print colours_in_db
else:
    # there are no colours - go fetch some!
    colour_index = lxml.html.fromstring(scraperwiki.scrape('http://dribbble.com/colors'))
    for el in colour_index.cssselect("ul.color-chips a"):
        print el
        scraperwiki.sqlite.save(unique_keys=['colour'], 
        data={
            'colour': el.text_content(), 
            'row_created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
        table_name='colours')

import scraperwiki
import datetime
import lxml.html

debug = 0

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `colours` (`colour` text, `row_created` text)')
if debug:
    scraperwiki.sqlite.execute('DELETE FROM colours')
scraperwiki.sqlite.commit()

colours_in_db = scraperwiki.sqlite.select('* from colours')

if len(colours_in_db):
    # there are colours in the database - use them!
    print colours_in_db
else:
    # there are no colours - go fetch some!
    colour_index = lxml.html.fromstring(scraperwiki.scrape('http://dribbble.com/colors'))
    for el in colour_index.cssselect("ul.color-chips a"):
        print el
        scraperwiki.sqlite.save(unique_keys=['colour'], 
        data={
            'colour': el.text_content(), 
            'row_created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
        table_name='colours')

