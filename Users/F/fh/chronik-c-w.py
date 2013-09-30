import scraperwiki
import lxml.html
import re

try:
    scraperwiki.sqlite.execute("drop table if exists 'chronik-cw'") 
    scraperwiki.sqlite.commit()
except:
    print 'e'


try:
    scraperwiki.sqlite.execute("""
        create table 'chronik-cw'
        ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."


html = scraperwiki.scrape("http://citywest.noblogs.org/chronologie/")
root = lxml.html.fromstring(html) 

i = 0

for el in root.cssselect('.entry-content h3#2012'): 
    #print el.toS
    print lxml.html.tostring(el)
    print el.text

    ela= el.getnext()
    #print lxml.html.tostring(ela)

    for el1 in ela.cssselect('ol li'): 
        #print lxml.html.tostring(el1.cssselect('strong'))
        #print el1['strong']

        #print lxml.html.tostring(el1)
        txt1 = el1.text_content()
        txt = txt1.encode('utf-8')

        p = re.compile('(\S+|\S+\s+)(straße|strasse|str\.?|weg|gasse|allee|ufer|platz|damm|ring)(\s+|\.{1}\s+)\d*', re.I)
        m = p.search(txt)
        #if ('campingplatz' or 'spielplatz') in m.lower():
        #    m = None

        print txt

        if m:
            print m.group()
        else:
            print 'No match'



        #txt = lxml.html.tostring(el1)
        #print el1.text
    #fields = tr.cssselect('td[valign="top"]')
    #i += 1

    #if i < 10:
    #    data = {
    #        'id' : i,
    #        'date' : fields[0].text_content(),
    #        'city' : 'Berlin Neukölln',
    #        'place' : fields[1].text_content(),
    #        'description' : fields[2].text_content()
    #    }
    #    print data
    #scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='chronik-ana')

import scraperwiki
import lxml.html
import re

try:
    scraperwiki.sqlite.execute("drop table if exists 'chronik-cw'") 
    scraperwiki.sqlite.commit()
except:
    print 'e'


try:
    scraperwiki.sqlite.execute("""
        create table 'chronik-cw'
        ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."


html = scraperwiki.scrape("http://citywest.noblogs.org/chronologie/")
root = lxml.html.fromstring(html) 

i = 0

for el in root.cssselect('.entry-content h3#2012'): 
    #print el.toS
    print lxml.html.tostring(el)
    print el.text

    ela= el.getnext()
    #print lxml.html.tostring(ela)

    for el1 in ela.cssselect('ol li'): 
        #print lxml.html.tostring(el1.cssselect('strong'))
        #print el1['strong']

        #print lxml.html.tostring(el1)
        txt1 = el1.text_content()
        txt = txt1.encode('utf-8')

        p = re.compile('(\S+|\S+\s+)(straße|strasse|str\.?|weg|gasse|allee|ufer|platz|damm|ring)(\s+|\.{1}\s+)\d*', re.I)
        m = p.search(txt)
        #if ('campingplatz' or 'spielplatz') in m.lower():
        #    m = None

        print txt

        if m:
            print m.group()
        else:
            print 'No match'



        #txt = lxml.html.tostring(el1)
        #print el1.text
    #fields = tr.cssselect('td[valign="top"]')
    #i += 1

    #if i < 10:
    #    data = {
    #        'id' : i,
    #        'date' : fields[0].text_content(),
    #        'city' : 'Berlin Neukölln',
    #        'place' : fields[1].text_content(),
    #        'description' : fields[2].text_content()
    #    }
    #    print data
    #scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='chronik-ana')

