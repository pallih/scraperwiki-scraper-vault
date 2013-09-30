import mechanize, string, sys, re, os
print "start"
from lxml.html import parse, tostring, fromstring
from scraperwiki import sqlite, metadata
from scraperwiki.geo import gb_postcode_to_latlng

re_time = re.compile('^\s*([\d ]\d[:.]\d\d)?\xa0\s*(\d\d[:.]\d\d)?\s*$')
days = set(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

br = mechanize.Browser()
br.addheaders = [("Accept", "text/html"),]
br.set_handle_robots(False)

postcode = '/rmg/finder/po/POFindTheNearestFormHandler.value.postcode'
office_type = '/rmg/finder/po/POFindTheNearestFormHandler.value.productid'
url = 'http://www.postoffice.co.uk/portal/po/finder'
blank = u'\n                        \xa0\n                    '
print url

class SearchErrors(Exception):
    pass

def parse_page(page):
    root = fromstring(page)
    results = root.find_class('bf-results')
    if len(results) == 0:
        return
    assert len(results) == 1
    for row in results[0].find_class('bf-results-row'):
        cur = {}
        assert row.tag == 'tr' and row[1].tag == 'td' and row[1][0].tag == 'strong'
        cur['name'] = row[1][0].text
        cur['address'] = [i.tail.strip() for i in row[1][1:-2]]
        cur['postcode'] = row[1][-1].text
        assert row[3].tag == 'td'

        ot_table = row[3][0]
        assert ot_table.tag == 'table' and ot_table.attrib['class'] == 'bf-opening-time'
        assert ot_table[0].tag == 'tr'
        assert ot_table[0][0].tag == 'th'
        assert ot_table[0][0].text == 'Opening hours'
        if len(ot_table[0]) != 1:
            assert len(ot_table[0]) == 2
            assert ot_table[0][1].tag == 'th'
            assert ot_table[0][1].attrib['class'] == 'bf-opening-time-lunch-cell'
            assert ot_table[0][1].text == 'Lunch'

        times = []
        for tr in ot_table[1:]:
            assert tr.tag == 'tr'
            assert tr[0].tag == 'td'
            assert tr[0].text[-1] == u'\xa0'
            day = tr[0].text[:-1]
            day = day[0] + day[1:].lower()
            assert day in days

            assert tr[1].tag == 'td'
            found = [day, None, None, None, None]
            if tr[1].text != blank:
                m = re_time.match(tr[1].text)
                found[1] = m.group(1)
                found[2] = m.group(2)
            if len(tr) != 2 and tr[2].text != blank:
                assert len(tr) == 3
                m = re_time.match(tr[2].text)
                found[3] = m.group(1)
                found[4] = m.group(2)
            times.append(tuple(found))

        cur['times'] = times
        yield cur

def read_town(town):
    br.open(url)

    assert br.viewing_html()
    br.select_form(name='finderForm')
    br[postcode] = town
    print br[office_type]
    br[office_type] = ['12']
    res2 = br.submit()
    assert br.viewing_html()

    page_num = 1
    #print res2.info()  # headers
    while True:
        page = res2.read()
        assert page
        if 'The details you have entered did not find any matches.' in page:
            print town, page_num, 'no results'
            assert page_num == 1
            return
        print town, page_num
        if 'bf-results' not in page:
            raise SearchErrors
        for po in parse_page(page):
            latlng=gb_postcode_to_latlng(po['postcode'])
            scraperwiki.sqlite.save(unique_keys=['name', 'postcode'], data=po, latlng=latlng)

        page_num += 1

        try:
            res2 = br.follow_link(text_regex='^next')
        except mechanize.LinkNotFoundError:
            break
        assert br.viewing_html()
            
bad_towns = []
def do_search(base):
    error = False
    for l in string.lowercase:
        town = base + l
        try:
            print "Trying %s" % town
            read_town(town)
        except SearchErrors:
            error = True
            do_search(town)
    if not error and base != '':
        bad_towns.append(base)
            
print "start"
do_search('')
metadata.save('bad_towns', bad_towns)
import mechanize, string, sys, re, os
print "start"
from lxml.html import parse, tostring, fromstring
from scraperwiki import sqlite, metadata
from scraperwiki.geo import gb_postcode_to_latlng

re_time = re.compile('^\s*([\d ]\d[:.]\d\d)?\xa0\s*(\d\d[:.]\d\d)?\s*$')
days = set(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

br = mechanize.Browser()
br.addheaders = [("Accept", "text/html"),]
br.set_handle_robots(False)

postcode = '/rmg/finder/po/POFindTheNearestFormHandler.value.postcode'
office_type = '/rmg/finder/po/POFindTheNearestFormHandler.value.productid'
url = 'http://www.postoffice.co.uk/portal/po/finder'
blank = u'\n                        \xa0\n                    '
print url

class SearchErrors(Exception):
    pass

def parse_page(page):
    root = fromstring(page)
    results = root.find_class('bf-results')
    if len(results) == 0:
        return
    assert len(results) == 1
    for row in results[0].find_class('bf-results-row'):
        cur = {}
        assert row.tag == 'tr' and row[1].tag == 'td' and row[1][0].tag == 'strong'
        cur['name'] = row[1][0].text
        cur['address'] = [i.tail.strip() for i in row[1][1:-2]]
        cur['postcode'] = row[1][-1].text
        assert row[3].tag == 'td'

        ot_table = row[3][0]
        assert ot_table.tag == 'table' and ot_table.attrib['class'] == 'bf-opening-time'
        assert ot_table[0].tag == 'tr'
        assert ot_table[0][0].tag == 'th'
        assert ot_table[0][0].text == 'Opening hours'
        if len(ot_table[0]) != 1:
            assert len(ot_table[0]) == 2
            assert ot_table[0][1].tag == 'th'
            assert ot_table[0][1].attrib['class'] == 'bf-opening-time-lunch-cell'
            assert ot_table[0][1].text == 'Lunch'

        times = []
        for tr in ot_table[1:]:
            assert tr.tag == 'tr'
            assert tr[0].tag == 'td'
            assert tr[0].text[-1] == u'\xa0'
            day = tr[0].text[:-1]
            day = day[0] + day[1:].lower()
            assert day in days

            assert tr[1].tag == 'td'
            found = [day, None, None, None, None]
            if tr[1].text != blank:
                m = re_time.match(tr[1].text)
                found[1] = m.group(1)
                found[2] = m.group(2)
            if len(tr) != 2 and tr[2].text != blank:
                assert len(tr) == 3
                m = re_time.match(tr[2].text)
                found[3] = m.group(1)
                found[4] = m.group(2)
            times.append(tuple(found))

        cur['times'] = times
        yield cur

def read_town(town):
    br.open(url)

    assert br.viewing_html()
    br.select_form(name='finderForm')
    br[postcode] = town
    print br[office_type]
    br[office_type] = ['12']
    res2 = br.submit()
    assert br.viewing_html()

    page_num = 1
    #print res2.info()  # headers
    while True:
        page = res2.read()
        assert page
        if 'The details you have entered did not find any matches.' in page:
            print town, page_num, 'no results'
            assert page_num == 1
            return
        print town, page_num
        if 'bf-results' not in page:
            raise SearchErrors
        for po in parse_page(page):
            latlng=gb_postcode_to_latlng(po['postcode'])
            scraperwiki.sqlite.save(unique_keys=['name', 'postcode'], data=po, latlng=latlng)

        page_num += 1

        try:
            res2 = br.follow_link(text_regex='^next')
        except mechanize.LinkNotFoundError:
            break
        assert br.viewing_html()
            
bad_towns = []
def do_search(base):
    error = False
    for l in string.lowercase:
        town = base + l
        try:
            print "Trying %s" % town
            read_town(town)
        except SearchErrors:
            error = True
            do_search(town)
    if not error and base != '':
        bad_towns.append(base)
            
print "start"
do_search('')
metadata.save('bad_towns', bad_towns)
