# -*- coding: utf-8 -*-
import scraperwiki
import lxml.html
#import requests
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone
from collections import defaultdict
from lxml.html import fromstring,tostring
import re

# http://www.kettering.gov.uk/site/scripts/planning_list.php?fromDay=05&fromMonth=04&fromYear=2012&toDay=12&toMonth=04&toYear=2012&submitDateWeekly=Go

DATE_FORMAT = "%d/%m/%Y"
tz = timezone('Europe/London')
rfc3339_date = "%Y-%m-%dT%H:%M:%SZ"
minus_60_days = (date.today() + relativedelta( days = -60 )).strftime(DATE_FORMAT)
test_date = '01/01/1998'

today_date = date.today().strftime(DATE_FORMAT)
is_date_regex = re.compile("^(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/[0-9]{4}$") # match dd/mm/yyyy, requiring leading zeros (http://answers.oreilly.com/topic/226-how-to-validate-traditional-date-formats-with-regular-expressions/)
replacements = {' ':'_','(':'',')':'','º'.decode('utf-8'):''}


def replace_all(text, dic):
    for i, j in dic.iteritems():
            text = text.replace(i, j)
    return text

def table_to_list(table):
    dct = table_to_2d_dict(table)
    return list(iter_2d_dict(dct))

def table_to_2d_dict(table):
    result = defaultdict(lambda : defaultdict(unicode))
    for row_i, row in enumerate(table.xpath('./tr')):
        for col_i, col in enumerate(row.xpath('./td|./th')):
            colspan = int(col.get('colspan', 1))
            rowspan = int(col.get('rowspan', 1))
            col_data = col.text_content()
            while row_i in result and col_i in result[row_i]:
                col_i += 1
            for i in range(row_i, row_i + rowspan):
                for j in range(col_i, col_i + colspan):
                    result[i][j] = col_data
    return result

def iter_2d_dict(dct):
    for i, row in sorted(dct.items()):
        cols = []
        for j, col in sorted(row.items()):
            cols.append(col)
        yield cols

def get_dt(date_string, date_format=DATE_FORMAT): # taken from scraperwiki.com/scrapers/utility_library/
    try:
        dt = datetime.strptime(date_string, date_format)
        return dt.date()
    except:
        return None

def test_dt(date_to_test, ref_date, date_format=DATE_FORMAT):
    try:
        test_dt = datetime.strptime(date_to_test, date_format)
        ref_dt = datetime.strptime(ref_date, date_format)
        if test_dt > ref_dt:
            return 1
        elif test_dt < ref_dt:
            return -1
        elif test_dt == ref_dt:
            return 0
        else:
            return None
    except:
        return None

def process(uid, url):
    record = {}
    record['url'] = url
    record['uid'] = uid
    record['date_scraped'] = datetime.now(tz).strftime(rfc3339_date)
    html = scraperwiki.scrape(url)
    doc = lxml.html.fromstring(html)

    #Application details
    for table_el in doc.xpath('//table[@summary="Planning application Details"]/tbody'):
        table = table_to_list(table_el)
        for item in table[:-2]:
            #if item[0] in allowed_keys:
            record[replace_all(item[0].strip().lower(),replacements)] = item[1].strip()

    #Application dates
    for table_el in doc.xpath('//table[@summary="key application dates"]/tbody'):
        table = table_to_list(table_el)      
        for item in table:
            if is_date_regex.search(item[1].strip()):
                record[replace_all(item[0].strip().lower(),replacements)] = str(get_dt(str(item[1].strip()),DATE_FORMAT))
            else:
                record[str(replace_all(item[0].strip().lower(),replacements))] = item[1].strip()
    #Rename keys that need renaming
    if 'location' in record:
        record['address'] = record.pop('location')
    if 'proposal' in record:
        record['description'] = record.pop('proposal')
    if 'decided_on' in record:
        record['decision_date'] = record.pop('decided_on')
    if 'validation/registration_date' in record:
        record['date_validated'] = record.pop('validation/registration_date')
    if 'neighbours/consultations_sent_on' in record:
        record['neighbour_consultation_start_date'] = record.pop('neighbours/consultations_sent_on')
    if 'expiry_date_for_neighbours/consultations' in record:
        record['neighbour_consultation_end_date'] = record.pop('expiry_date_for_neighbours/consultations')
    if 'advertised_on' in record:
        record['last_advertised_date'] = record.pop('advertised_on')

    #Start date
    if record['date_received']:
        record['start_date'] = record['date_received']
    else:
        record['start_date'] = record['date_validated']
    scraperwiki.sqlite.save(unique_keys=['uid'], data=record, verbose=0) 
    

def get(from_date,to_date,url,counter):
    if counter == '':
        counter = 0
    if url == '':
        url =  'http://www.kettering.gov.uk/site/scripts/planning_list.php?fromDay=%s&fromMonth=%s&fromYear=%s&toDay=%s&toMonth=%s&toYear=%s&submitDateWeekly=Go' % (from_date.split('/')[0],from_date.split('/')[1],from_date.split('/')[2],to_date.split('/')[0],to_date.split('/')[1],to_date.split('/')[2])
        #url = 'http://www.kettering.gov.uk/site/scripts/planning_list.php?fromDay=01&fromMonth=04&fromYear=2004&toDay=08&toMonth=04&toYear=2004&submitDateWeekly=Go'
    results = scraperwiki.scrape(url)
    root = lxml.html.fromstring(results)
    table = root.xpath('//table/tbody/tr')
    for tr in table:
        uid = tr[0][0].text.strip()
        detail_url = tr[0][0].attrib['href']
        process(uid, detail_url)
        counter = counter+1
    if root.xpath('//a[contains(text(),"Next")]'):
        get('','',root.xpath('//a[contains(text(),"Next")]')[0].attrib['href'],counter)
    else:
        print 'Done. Fetched ',counter,' records.'
    
print 'Fetching last 60 days'       
get(minus_60_days,today_date,'','')


last_old = scraperwiki.sqlite.get_var('last_old')
minus_60_old_days = (datetime.strptime(last_old,DATE_FORMAT) + relativedelta( days = -60 )).strftime(DATE_FORMAT)
    
if test_dt(last_old, test_date) == 1:
    print 'Fetching 60 more days of old ones, starting from', last_old, ' and going to ', minus_60_old_days
    get(minus_60_old_days,last_old,'','')
    scraperwiki.sqlite.save_var('last_old', minus_60_old_days) 
else:
    print 'Old collection is permanently done!'

print
print '--- Done for today ---'
 