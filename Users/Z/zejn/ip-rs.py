import scraperwiki
import urllib
import datetime
import lxml.html
import re
import scraperwiki.sqlite
import sys

BASE_URL = "https://www.ip-rs.si/informacije-javnega-znacaja/iskalnik-po-odlocbah/odlocbe-informacije-javnega-znacaja/"
ba_url = "https://www.ip-rs.si/nc/informacije-javnega-znacaja/iskalnik-po-odlocbah/odlocbe-informacije-javnega-znacaja/?tx_jzdecisions_pi1%5Bsort%5D=date%3A1&tx_jzdecisions_pi1%5Bpointer%5D=10&tx_jzdecisions_pi1%5Bmode%5D=IEFORCBzdGF0dXMgTk9UIGluICgnNScp"
#HIST_BASE_URL = scraperwiki.sqlite.get_var("LAST_URL", ba_url)
LAST_URL = None

END_OF_TIME = '9999-12-31'
fetched_count = 0

def toascii(s):
    return s.strip().replace(u'\u010d', 'c').replace(u'\u0161', 's').replace(u'\u017e','z').replace(' ', '_')

def get_page(url):
    global fetched_count
    fetched_count += 1
    print 'Fetching... %s %s' % (fetched_count, url)
    doc = lxml.html.parse(urllib.urlopen(url))
    html = doc.getroot()
    html.make_links_absolute(url)
    return html

def get_odlocbe_list(days=90):
    global LAST_URL
    page = get_page(BASE_URL)
    tday = datetime.date.today()
    odlocbe = []
    parsed_date = tday
    while parsed_date > tday - datetime.timedelta(days):
        rows = page.xpath('//table[@class="odlocbe"]/tr')[1:]
        for row in rows:
            rd_, rna, rsv, rk, rst = row.xpath('./td')
            dt = datetime.datetime.strptime(rd_.text, '%d.%m.%Y')
            parsed_date = datetime.date(dt.year, dt.month, dt.day)
            rd = parsed_date.strftime('%Y-%m-%d')
            rn = rna.xpath('./a')[0]
            rec = {'datum': rd,
                'naslov': rn.text.strip(),
                'url': rn.attrib['href'],
                'stevilka': rsv.text.strip(),
                'kategorija': rk.text != None and rk.text.strip() or '',
                'status': rst.text.strip(),
            }
            odlocbe.append(rec)
        next_page_a = page.xpath('//a[text()="Naslednja >"]')
        if next_page_a:
            next_page_url = next_page_a[0].attrib['href']
            del page
            page = get_page(next_page_url)
            LAST_URL = next_page_url
        else:
            break
    print "Scraped until", parsed_date
    scraperwiki.sqlite.save_var("LAST_DATE", parsed_date)
    return odlocbe

def add_odlocba_info(odl):
    odl_url = re.sub('&cHash=[0-9a-f]*', '&cHash=1', odl['url'])
    page = get_page(odl_url)
    try:
        div = page.xpath('//div[@class="tx-jzdecisions-pi1"]')[0]
    except IndexError:
        print >> sys.stderr, "Failed %s", odl['stevilka'], odl['datum']
        return
    odl_info, odl_text, _ = div.xpath('.//table/tr/td')
    odl_info_dict = {}
    for b in odl_info.getchildren():
        if b.tag != 'b':
            continue
        if b.text == None and b.tail.strip() == '':
            continue
        k = toascii(b.text.rstrip(':').lower())
        v = b.tail != None and b.tail.strip() or ''
        odl_info_dict[k] = v
    odl_text.tag = 'div'
    odl_full_text = lxml.html.tostring(odl_text)
    
    odl['full_text'] = odl_full_text
    odl['info_datum'] = odl_info_dict['datum']
    odl['info_naslov'] = odl_info_dict['naslov']
    odl['info_stevilka'] = odl_info_dict['stevilka']
    odl['info_kategorija'] = odl_info_dict['kategorija']
    odl['info_status'] = odl_info_dict['status']

def merge_records(records):
    print 'Saving...'
    tday = datetime.date.today().strftime('%Y-%m-%d')
    import scraperwiki.sqlite
    retired_count = 0
    new_count = 0
    all_count = 0
    retire = []
    new = []
    db_records_list = scraperwiki.sqlite.select('* from swdata')
    #db_records_list = [] # used for db initialization
    for r in db_records_list:
        del r['valid_start'] # complicates comparison
    db_records = dict([((r['stevilka'], r['valid_end']), r) for r in db_records_list])
    assert len(db_records.keys()) == len(db_records_list), "Record count mismatch, something wrong with db?"
    for rec in records:
        items = rec.items()
        where = ' and '.join(['"%s"=?' % i[0] for i in items])
        r2 = rec.copy()
        r2['valid_end'] = END_OF_TIME
        if db_records.get((rec['stevilka'], END_OF_TIME)) == r2:
            # record still valid
            pass
        else:
            if db_records.get((rec['stevilka'], END_OF_TIME)):
                # record changed, first retire old record
                retire.append(rec['stevilka'])
            # add new record - in both cases
            rec['valid_start'] = tday
            rec['valid_end'] = END_OF_TIME
            new.append(rec)
            new_count += 1
        all_count += 1
        if all_count % 200 == 0:
            print "Sorting: %s processed, %s retired, %s new" % (all_count, retired_count, new_count)
    print 'Saving to SQL'
    if retire:
        retire_sql = ', '.join(['?' for i in retire])
        scraperwiki.sqlite.execute('update swdata set valid_end=? where stevilka in (' + retire_sql + ') and valid_end=?',
            [tday] + retire  + [END_OF_TIME])
        scraperwiki.sqlite.commit()
    if new:
        scraperwiki.sqlite.save(unique_keys=['stevilka', 'valid_end'], data=new)
    
    print '... done.'   


# main

hist = False # get historic stuff or not?
if hist:
    n = scraperwiki.sqlite.get_var("N", 5)
    BASE_URL = HIST_BASE_URL
else:
    n = 2

odlocbe_list = get_odlocbe_list(60*n)
for odl in odlocbe_list:
    add_odlocba_info(odl)
merge_records(odlocbe_list)

if hist:
    # ok done, update for next run
    scraperwiki.sqlite.save_var("N", n+1)
    scraperwiki.sqlite.save_var("LAST_URL", LAST_URL)
