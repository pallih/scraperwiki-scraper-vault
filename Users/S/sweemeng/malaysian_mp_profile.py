import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
import json
import uuid

def get_img(tr):
    img = tr.find('img')
    return img['src']

def get_profile(url):
    data = {}
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    # The containing main div
    main_div = soup.find('div',{'id':'center-columns'})
    
    # inner div
    inner_div = main_div.find('div',{'class':'parfont'})
    
    # table with table
    table = inner_div.find('table').find('table')
    
    tr = table.findAll('tr')
    data['img'] = get_img(tr[0])
    
    for i in tr[3:]:
        td = i.findAll('td')
        data[td[0].text.replace(' ','_').replace('.','')] = td[1].text
    
    return data

def main():
    scraperwiki.sqlite.attach('malaysian_members_of_parliment_contact_url','url_list')
    scraperwiki.sqlite.attach('mys_seats','seats')
    links = scraperwiki.sqlite.select('key,url from url_list.swdata')
    existing = scraperwiki.sqlite.show_tables()
    if existing:
        val = scraperwiki.sqlite.select('max(key) from swdata')
        max_val = int(val[0]['max(key)'])
    else:
        
        max_val = 0

    print max_val

    for i in links:
        if int(i['key']) < max_val:
            continue
        d = get_profile(i['url'])
        d['key'] = int(i['key'])
        print 'Before :%s' % (d['Parlimen'])
        print 'After :%s' % str(d['Parlimen'][1:])
        print 'Fault :%s' % d['Nama']
        try:
            d['Parlimen'] = int(d['Parlimen'][1:])
        except:
            query = 'select id from seats.parliament_seats where name = :name'
            get_id = scraperwiki.sqlite.execute(query,{'name':d['Kawasan'].lower()})
            d['Parlimen'] = get_id['data'][0]['id']

        #print d['key']
        scraperwiki.sqlite.save(unique_keys=['key'],data=d)

def test_db():
    test_val = scraperwiki.sqlite.show_tables()
    print test_val

main()import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
import json
import uuid

def get_img(tr):
    img = tr.find('img')
    return img['src']

def get_profile(url):
    data = {}
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    # The containing main div
    main_div = soup.find('div',{'id':'center-columns'})
    
    # inner div
    inner_div = main_div.find('div',{'class':'parfont'})
    
    # table with table
    table = inner_div.find('table').find('table')
    
    tr = table.findAll('tr')
    data['img'] = get_img(tr[0])
    
    for i in tr[3:]:
        td = i.findAll('td')
        data[td[0].text.replace(' ','_').replace('.','')] = td[1].text
    
    return data

def main():
    scraperwiki.sqlite.attach('malaysian_members_of_parliment_contact_url','url_list')
    scraperwiki.sqlite.attach('mys_seats','seats')
    links = scraperwiki.sqlite.select('key,url from url_list.swdata')
    existing = scraperwiki.sqlite.show_tables()
    if existing:
        val = scraperwiki.sqlite.select('max(key) from swdata')
        max_val = int(val[0]['max(key)'])
    else:
        
        max_val = 0

    print max_val

    for i in links:
        if int(i['key']) < max_val:
            continue
        d = get_profile(i['url'])
        d['key'] = int(i['key'])
        print 'Before :%s' % (d['Parlimen'])
        print 'After :%s' % str(d['Parlimen'][1:])
        print 'Fault :%s' % d['Nama']
        try:
            d['Parlimen'] = int(d['Parlimen'][1:])
        except:
            query = 'select id from seats.parliament_seats where name = :name'
            get_id = scraperwiki.sqlite.execute(query,{'name':d['Kawasan'].lower()})
            d['Parlimen'] = get_id['data'][0]['id']

        #print d['key']
        scraperwiki.sqlite.save(unique_keys=['key'],data=d)

def test_db():
    test_val = scraperwiki.sqlite.show_tables()
    print test_val

main()