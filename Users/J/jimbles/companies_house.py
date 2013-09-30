import scraperwiki
import mechanize
import tempfile
import zipfile
import xlrd
import csv
import time

def checkpoint_set (newstate, newzip, newrow):
    global state, point_zip, point_row
    state = newstate
    point_zip = newzip
    point_row = newrow
    scraperwiki.sqlite.save_var ('state', state, verbose=0)
    scraperwiki.sqlite.save_var ('zip', point_zip, verbose=0)
    scraperwiki.sqlite.save_var ('row', point_row, verbose=0)

def checkpoint_get ():
    global state, point_zip, point_row
    state = scraperwiki.sqlite.get_var ('state', 'get', verbose=0)
    point_zip = scraperwiki.sqlite.get_var ('zip', 0, verbose=0)
    point_row = scraperwiki.sqlite.get_var ('row', 0, verbose=0)

def lock_aware_save(unique_keys, data, table_name="swdata", verbose=2, date=None, delay_ms=100, max_tries=10):
    tries = 0
    while tries < max_tries:
        try:
            scraperwiki.sqlite.save (unique_keys, data, table_name, verbose, date)
        except scraperwiki.sqlite.SqliteError:
            tries += 1
            if tries >= max_tries:
                raise
            time.sleep (delay_ms/1000)
    if tries > 0:
        print 'Got lock after %d tries' % (tries)

#checkpoint_set ('get', 0, 0)
checkpoint_get ()
print '%s Zip %d Row %d' % (state, point_zip, point_row)

src = br = mechanize.Browser (factory=mechanize.RobustFactory())
br.open ('http://download.companieshouse.gov.uk/en_output.html')
zips = ['http://download.companieshouse.gov.uk/'+link.url for link in br.links(url_regex='.zip')]
buf_comps = []
buf_prev = []
for z, fl in enumerate(zips):
    if z >= point_zip:
        print 'Downloading '+fl
        t_fl = tempfile.NamedTemporaryFile(suffix='.zip',delete=False)
        t_fl.write (scraperwiki.scrape(fl))
        t_fl.close()
        print 'Opening '+t_fl.name
        zf = zipfile.ZipFile (t_fl.name)
        csv_fl = zf.open(zf.namelist()[0])
        csv_r = csv.reader (csv_fl)
        headers = csv_r.next()
        print headers
        print 'Parsing '+zf.namelist()[0]
        for i in range(0,len(headers)):
            while headers[i][:1] == ' ': #strip leading space
                headers[i] = headers[i][1:]
            headers[i] = headers[i].replace('.','_')

        for r, row in enumerate(csv_r):
            if r >= point_row:
                if (r % 1000) == 0:
                    print 'Row %d' % (r)
                    if len(buf_comps) > 0:
                        try:
                            scraperwiki.sqlite.save (unique_keys=['CompanyNumber'], data=buf_comps, table_name='companies', verbose=0)
                        except scraperwiki.sqlite.SqliteError:
                            print 'Save deferred due to locking'
                        else:
                            buf_comps = []
                    if len(buf_prev) > 0:
                        try:
                            scraperwiki.sqlite.save (unique_keys=['CompanyNumber', 'N'], data=buf_prev, table_name='prev_names', verbose=0)
                        except scraperwiki.sqlite.SqliteError:
                            print 'Save deferred due to locking'
                        else:
                            buf_prev = []
                    if len(buf_prev) == 0 and len(buf_comps) == 0:
                        checkpoint_set ('get', z, r)
                rv = [str(v) for v in row] #force all to string
                d = dict(zip(headers,rv))
                for i in range(1,10):
                    kname = 'PreviousName_'+str(i)+'_CompanyName'
                    kdate = 'PreviousName_'+str(i)+'_CONDATE'
                    if d[kdate] != '':
                        buf_prev.append ({'CompanyNumber':str(d['CompanyNumber']), 'N':int(i), 'CompanyName':str(d[kname]), 'ConDate':str(d[kdate])})
                    del d[kname]
                    del d[kdate]
                buf_comps.append (d)
        try:
            if len(buf_comps) > 0:
                scraperwiki.sqlite.save (unique_keys=['CompanyNumber'], data=buf_comps, table_name='companies', verbose=0)
        except scraperwiki.sqlite.SqliteError:
            pass
        else:
            buf_comps = []
            try:
                if len(buf_prev) > 0:
                    scraperwiki.sqlite.save (unique_keys=['CompanyNumber', 'N'], data=buf_prev, table_name='prev_names', verbose=0)
            except scraperwiki.sqlite.SqliteError:
                pass
            else:
                buf_prev = []
                checkpoint_set ('get', z+1, 0)

import scraperwiki
import mechanize
import tempfile
import zipfile
import xlrd
import csv
import time

def checkpoint_set (newstate, newzip, newrow):
    global state, point_zip, point_row
    state = newstate
    point_zip = newzip
    point_row = newrow
    scraperwiki.sqlite.save_var ('state', state, verbose=0)
    scraperwiki.sqlite.save_var ('zip', point_zip, verbose=0)
    scraperwiki.sqlite.save_var ('row', point_row, verbose=0)

def checkpoint_get ():
    global state, point_zip, point_row
    state = scraperwiki.sqlite.get_var ('state', 'get', verbose=0)
    point_zip = scraperwiki.sqlite.get_var ('zip', 0, verbose=0)
    point_row = scraperwiki.sqlite.get_var ('row', 0, verbose=0)

def lock_aware_save(unique_keys, data, table_name="swdata", verbose=2, date=None, delay_ms=100, max_tries=10):
    tries = 0
    while tries < max_tries:
        try:
            scraperwiki.sqlite.save (unique_keys, data, table_name, verbose, date)
        except scraperwiki.sqlite.SqliteError:
            tries += 1
            if tries >= max_tries:
                raise
            time.sleep (delay_ms/1000)
    if tries > 0:
        print 'Got lock after %d tries' % (tries)

#checkpoint_set ('get', 0, 0)
checkpoint_get ()
print '%s Zip %d Row %d' % (state, point_zip, point_row)

src = br = mechanize.Browser (factory=mechanize.RobustFactory())
br.open ('http://download.companieshouse.gov.uk/en_output.html')
zips = ['http://download.companieshouse.gov.uk/'+link.url for link in br.links(url_regex='.zip')]
buf_comps = []
buf_prev = []
for z, fl in enumerate(zips):
    if z >= point_zip:
        print 'Downloading '+fl
        t_fl = tempfile.NamedTemporaryFile(suffix='.zip',delete=False)
        t_fl.write (scraperwiki.scrape(fl))
        t_fl.close()
        print 'Opening '+t_fl.name
        zf = zipfile.ZipFile (t_fl.name)
        csv_fl = zf.open(zf.namelist()[0])
        csv_r = csv.reader (csv_fl)
        headers = csv_r.next()
        print headers
        print 'Parsing '+zf.namelist()[0]
        for i in range(0,len(headers)):
            while headers[i][:1] == ' ': #strip leading space
                headers[i] = headers[i][1:]
            headers[i] = headers[i].replace('.','_')

        for r, row in enumerate(csv_r):
            if r >= point_row:
                if (r % 1000) == 0:
                    print 'Row %d' % (r)
                    if len(buf_comps) > 0:
                        try:
                            scraperwiki.sqlite.save (unique_keys=['CompanyNumber'], data=buf_comps, table_name='companies', verbose=0)
                        except scraperwiki.sqlite.SqliteError:
                            print 'Save deferred due to locking'
                        else:
                            buf_comps = []
                    if len(buf_prev) > 0:
                        try:
                            scraperwiki.sqlite.save (unique_keys=['CompanyNumber', 'N'], data=buf_prev, table_name='prev_names', verbose=0)
                        except scraperwiki.sqlite.SqliteError:
                            print 'Save deferred due to locking'
                        else:
                            buf_prev = []
                    if len(buf_prev) == 0 and len(buf_comps) == 0:
                        checkpoint_set ('get', z, r)
                rv = [str(v) for v in row] #force all to string
                d = dict(zip(headers,rv))
                for i in range(1,10):
                    kname = 'PreviousName_'+str(i)+'_CompanyName'
                    kdate = 'PreviousName_'+str(i)+'_CONDATE'
                    if d[kdate] != '':
                        buf_prev.append ({'CompanyNumber':str(d['CompanyNumber']), 'N':int(i), 'CompanyName':str(d[kname]), 'ConDate':str(d[kdate])})
                    del d[kname]
                    del d[kdate]
                buf_comps.append (d)
        try:
            if len(buf_comps) > 0:
                scraperwiki.sqlite.save (unique_keys=['CompanyNumber'], data=buf_comps, table_name='companies', verbose=0)
        except scraperwiki.sqlite.SqliteError:
            pass
        else:
            buf_comps = []
            try:
                if len(buf_prev) > 0:
                    scraperwiki.sqlite.save (unique_keys=['CompanyNumber', 'N'], data=buf_prev, table_name='prev_names', verbose=0)
            except scraperwiki.sqlite.SqliteError:
                pass
            else:
                buf_prev = []
                checkpoint_set ('get', z+1, 0)

