import scraperwiki
import lxml.html

#try:
#    scraperwiki.sqlite.execute("drop table if exists 'chronik-op'") 
#    scraperwiki.sqlite.commit()
#except:
#    print 'e'

#try:
#    scraperwiki.sqlite.execute("""
#        create table 'chronik-op'
#        ( 
#        id INTEGER PRIMARY KEY AUTOINCREMENT
#        )
#    """)
#except:
#    print "Table probably already exists."


html = scraperwiki.scrape("http://opferperspektive.de/event/events_by_criteria/1?note=%2A&location=%2A&page=9&year=2012")
root = lxml.html.fromstring(html) 

for row in root.cssselect('.opp_evt'): 
    heading = row.cssselect('.opp_heading .opp_event_location')
    event_title = row.cssselect('.opp_event_title')
    event_content = row.cssselect('.opp_event_content')
    src = row.cssselect('.opp_src')

    heading_fields1 = heading[0].text_content().split('»'.decode("utf-8"))
    heading_fields2 = heading_fields1[1].split('/'.decode("utf-8"))

    data = {
        'date' : heading_fields1[0].strip(),
        'city' : heading_fields2[0].strip(),
        'district' : heading_fields2[1].strip(),
        'country' : 'Germany', 
        'heading' : event_title[0].text_content(),
        'description' : event_content[0].text_content(),
        'src' : src[0].text_content().lstrip('(').rstrip(')')
    }
    print data
    scraperwiki.sqlite.save(unique_keys=[], data=data, table_name='chronik-op')

import scraperwiki
import lxml.html

#try:
#    scraperwiki.sqlite.execute("drop table if exists 'chronik-op'") 
#    scraperwiki.sqlite.commit()
#except:
#    print 'e'

#try:
#    scraperwiki.sqlite.execute("""
#        create table 'chronik-op'
#        ( 
#        id INTEGER PRIMARY KEY AUTOINCREMENT
#        )
#    """)
#except:
#    print "Table probably already exists."


html = scraperwiki.scrape("http://opferperspektive.de/event/events_by_criteria/1?note=%2A&location=%2A&page=9&year=2012")
root = lxml.html.fromstring(html) 

for row in root.cssselect('.opp_evt'): 
    heading = row.cssselect('.opp_heading .opp_event_location')
    event_title = row.cssselect('.opp_event_title')
    event_content = row.cssselect('.opp_event_content')
    src = row.cssselect('.opp_src')

    heading_fields1 = heading[0].text_content().split('»'.decode("utf-8"))
    heading_fields2 = heading_fields1[1].split('/'.decode("utf-8"))

    data = {
        'date' : heading_fields1[0].strip(),
        'city' : heading_fields2[0].strip(),
        'district' : heading_fields2[1].strip(),
        'country' : 'Germany', 
        'heading' : event_title[0].text_content(),
        'description' : event_content[0].text_content(),
        'src' : src[0].text_content().lstrip('(').rstrip(')')
    }
    print data
    scraperwiki.sqlite.save(unique_keys=[], data=data, table_name='chronik-op')

