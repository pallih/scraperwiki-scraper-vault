import mechanize, string, sys, re, os
print "start"
from lxml.html import parse, tostring, fromstring
from scraperwiki import metadata, sqlite
from scraperwiki.geo import gb_postcode_to_latlng
from time import sleep

re_time = re.compile('^\s*([\d ]\d[:.]\d\d)?\xa0\s*(\d\d[:.]\d\d)?\s*$')
days = set(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

br = mechanize.Browser()
br.addheaders = [("Accept", "text/html"),]
br.set_handle_robots(False)

postcode = 'postcode_or_town'
url = 'http://www.postoffice.co.uk/portal/po/finder'
url = 'http://www.postoffice.co.uk/branch-finder'
blank = u'\n                        \xa0\n                    '
print url

class SearchErrors(Exception):
    pass

def parse_page(page):
    root = fromstring(page)
    results = root.find_class('bf-results')
    if len(results) == 0:
        print 'bf-results not found'
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
    br.select_form(nr=1)
    br[postcode] = town
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
            print 'search error'
            raise SearchErrors
        print "calling parse_page"
        for po in parse_page(page):
            print po
            latlon=None
            for attempt in range(10):
                try:
                    latlon=gb_postcode_to_latlng(po['postcode'])
                    break
                except:
                    pass
                print 'gb_postcode_to_latlng fail for "%s", attempt %d' % (po['postcode'], attempt)
                sleep(10)
            if latlon:
                (po['lat'], po['lon'])=latlon
            sqlite.save(unique_keys=['name', 'postcode'], data=po)

        page_num += 1

        link_not_found = False
        for attempt in range(5):
            try:
                res2 = br.follow_link(text_regex='^next')
                break
            except mechanize.LinkNotFoundError:
                link_not_found = True
                break
            except URLError: # try again
                if attempt == 4:
                    raise
                print 'retry, attempt:', attempt
        if link_not_found:
            break
        assert br.viewing_html()
            
bad_towns = []
def do_search(base):
    error = False
    for l in string.lowercase:
        town = base + l
        try:
            read_town(town)
        except SearchErrors:
            error = True
            do_search(town)
    if not error and base != '':
        bad_towns.append(base)

print "start"
do_search('')
metadata.save('bad_towns', bad_towns)