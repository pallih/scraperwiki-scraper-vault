import scraperwiki
import lxml.html


def do_city(name, url):
    page = scraperwiki.scrape( url )
    dom = lxml.html.fromstring(page)
#    print name
#    print links
    for row in dom.cssselect('title'):
        title = row.text_content()
        city = title.split('-')[0][:-20].split(' ')[0]
        if len(title.split('-')[0][:-20].split(' ')) == 2:
            state = title.split('-')[0][:-20].split(' ')[-1]
        else:
            state = title.split('-')[0][:-20].split(' ')[1] + ' ' + title.split('-')[0][:-20].split(' ')[2]
        for row in dom.cssselect('tr'):
            print row[0].text_content()
            if len(row) > 1:
                scraperwiki.sqlite.save(['state','city','name'], {'state':state, 'city': city, 'name': row[0].text_content()}, table_name='major_cities')
                scraperwiki.sqlite.save(['text','location'], {'text':row[0].text_content(), 'location': "%s, %s, United States" % (city, state)}, table_name='city_list')

def do_state(state_name, url):
    page = scraperwiki.scrape( url )
    dom = lxml.html.fromstring(page)
    for row in dom.cssselect('tr'):
        if len(row) > 1:
            name = row[1].text_content()
            city = row[0].text_content()
            scraperwiki.sqlite.save(['state','city','name'], {'state':state_name, 'city':city, 'name':name}, table_name='states')
            scraperwiki.sqlite.save(['text','location'], {'text':name, 'location': "%s, %s, United States" % (city,state_name,)}, table_name='media_list')


html = scraperwiki.scrape("http://www.easymedialist.com/usa/index.html")
root = lxml.html.fromstring(html)
tables = root.cssselect('div.main table')
states = tables[0]
cities = tables[1]

for td in states.cssselect('td'):
    links = td.cssselect("a")
    for link in links:
        loc = link.text_content()
        url = link.attrib.get('href')
        do_state(loc, url)

for td in cities.cssselect('td'):
    links = td.cssselect("a")
    for link in links:
        loc = link.text_content()
        url = link.attrib.get('href')
        do_city(loc, url)


import scraperwiki
import lxml.html


def do_city(name, url):
    page = scraperwiki.scrape( url )
    dom = lxml.html.fromstring(page)
#    print name
#    print links
    for row in dom.cssselect('title'):
        title = row.text_content()
        city = title.split('-')[0][:-20].split(' ')[0]
        if len(title.split('-')[0][:-20].split(' ')) == 2:
            state = title.split('-')[0][:-20].split(' ')[-1]
        else:
            state = title.split('-')[0][:-20].split(' ')[1] + ' ' + title.split('-')[0][:-20].split(' ')[2]
        for row in dom.cssselect('tr'):
            print row[0].text_content()
            if len(row) > 1:
                scraperwiki.sqlite.save(['state','city','name'], {'state':state, 'city': city, 'name': row[0].text_content()}, table_name='major_cities')
                scraperwiki.sqlite.save(['text','location'], {'text':row[0].text_content(), 'location': "%s, %s, United States" % (city, state)}, table_name='city_list')

def do_state(state_name, url):
    page = scraperwiki.scrape( url )
    dom = lxml.html.fromstring(page)
    for row in dom.cssselect('tr'):
        if len(row) > 1:
            name = row[1].text_content()
            city = row[0].text_content()
            scraperwiki.sqlite.save(['state','city','name'], {'state':state_name, 'city':city, 'name':name}, table_name='states')
            scraperwiki.sqlite.save(['text','location'], {'text':name, 'location': "%s, %s, United States" % (city,state_name,)}, table_name='media_list')


html = scraperwiki.scrape("http://www.easymedialist.com/usa/index.html")
root = lxml.html.fromstring(html)
tables = root.cssselect('div.main table')
states = tables[0]
cities = tables[1]

for td in states.cssselect('td'):
    links = td.cssselect("a")
    for link in links:
        loc = link.text_content()
        url = link.attrib.get('href')
        do_state(loc, url)

for td in cities.cssselect('td'):
    links = td.cssselect("a")
    for link in links:
        loc = link.text_content()
        url = link.attrib.get('href')
        do_city(loc, url)


