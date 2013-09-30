DATA_URL = 'http://www.ujp.gov.si/RPU/ListRpuTxt.aspx'
ENCODING = 'utf-8'
END_OF_TIME = '9999-12-31'

import urllib
import datetime
import scraperwiki

def get_data():
    print 'Fetching data from %s ...' % DATA_URL
    u = urllib.urlopen(DATA_URL)
    data = u.read()
    print '... done.'
    return data

def toascii(s):
    return s.strip().replace(u'\u010d', 'c').replace(u'\u0161', 's').replace(u'\u017e','z').replace(' ', '_')

def data_to_records(data):
    print 'Processing data...'
    lines = data.decode(ENCODING).split('\r\n')
    # first line is gibberish
    assert not ';' in lines[0], "First is record?"
    header = [str(toascii(i)) for i in lines[1].lower().split(';')]
    print header
    records = []
    data_lines = [i for i in lines[2:] if i]
    valid_end = END_OF_TIME
    for line in data_lines:
        rec = dict(zip(header, [i.strip() for i in line.split(';')]))
        rec['valid_end'] = valid_end
        records.append(rec)
    
    print '... done.'
    return records

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
    for r in db_records_list:
        del r['valid_start'] # complicates comparison
    db_records = dict([((r['maticna'], r['valid_end']), r) for r in db_records_list])
    assert len(db_records.keys()) == len(db_records_list), "Record count mismatch, something wrong with db?"
    for rec in records:
        items = rec.items()
        where = ' and '.join(['"%s"=?' % i[0] for i in items])
        r2 = rec.copy()
        r2['valid_end'] = END_OF_TIME
        if db_records.get((rec['maticna'], END_OF_TIME)) == r2: 
            # record still valid
            pass
        else:
            if db_records.get((rec['maticna'], END_OF_TIME)):
                # record changed, first retire old record
                retire.append(rec['maticna'])
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
        scraperwiki.sqlite.execute('update swdata set valid_end=? where maticna in (' + retire_sql + ') and valid_end=?', 
            [tday] + retire  + [END_OF_TIME])
        scraperwiki.sqlite.commit()
    if new:
        scraperwiki.sqlite.save(unique_keys=['maticna', 'valid_end'], data=new)
    
    print '... done.'    


data = get_data()
records = data_to_records(data)
merge_records(records)

    
DATA_URL = 'http://www.ujp.gov.si/RPU/ListRpuTxt.aspx'
ENCODING = 'utf-8'
END_OF_TIME = '9999-12-31'

import urllib
import datetime
import scraperwiki

def get_data():
    print 'Fetching data from %s ...' % DATA_URL
    u = urllib.urlopen(DATA_URL)
    data = u.read()
    print '... done.'
    return data

def toascii(s):
    return s.strip().replace(u'\u010d', 'c').replace(u'\u0161', 's').replace(u'\u017e','z').replace(' ', '_')

def data_to_records(data):
    print 'Processing data...'
    lines = data.decode(ENCODING).split('\r\n')
    # first line is gibberish
    assert not ';' in lines[0], "First is record?"
    header = [str(toascii(i)) for i in lines[1].lower().split(';')]
    print header
    records = []
    data_lines = [i for i in lines[2:] if i]
    valid_end = END_OF_TIME
    for line in data_lines:
        rec = dict(zip(header, [i.strip() for i in line.split(';')]))
        rec['valid_end'] = valid_end
        records.append(rec)
    
    print '... done.'
    return records

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
    for r in db_records_list:
        del r['valid_start'] # complicates comparison
    db_records = dict([((r['maticna'], r['valid_end']), r) for r in db_records_list])
    assert len(db_records.keys()) == len(db_records_list), "Record count mismatch, something wrong with db?"
    for rec in records:
        items = rec.items()
        where = ' and '.join(['"%s"=?' % i[0] for i in items])
        r2 = rec.copy()
        r2['valid_end'] = END_OF_TIME
        if db_records.get((rec['maticna'], END_OF_TIME)) == r2: 
            # record still valid
            pass
        else:
            if db_records.get((rec['maticna'], END_OF_TIME)):
                # record changed, first retire old record
                retire.append(rec['maticna'])
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
        scraperwiki.sqlite.execute('update swdata set valid_end=? where maticna in (' + retire_sql + ') and valid_end=?', 
            [tday] + retire  + [END_OF_TIME])
        scraperwiki.sqlite.commit()
    if new:
        scraperwiki.sqlite.save(unique_keys=['maticna', 'valid_end'], data=new)
    
    print '... done.'    


data = get_data()
records = data_to_records(data)
merge_records(records)

    
