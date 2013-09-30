encoding = 'utf-8'

#PO_zipurl = "http://www.gov.si/aplikacije/durs/PO.zip"
#FOzD_zipurl = "http://www.gov.si/aplikacije/durs/FOzD.zip"


PO_zipurl = "http://datoteke.durs.gov.si/DURS_zavezanci_PO.zip"
FOzD_zipurl = "http://datoteke.durs.gov.si/DURS_zavezanci_DEJ.zip"


LEGAL_ENTITY = "legal entity"
SOLE_PROPRIETOR = 'sole proprietor'

# ========================================
import datetime
import re
import tempfile
import urllib
import zipfile

def get_zip(url):
    print 'Fetching %s ...' % (url,)
    tmp = tempfile.NamedTemporaryFile(suffix='.zip')
    urllib.urlretrieve(url, tmp.name)
    print '... done.'
    return tmp

def get_records(fn, comp_type):
    print 'Parsing file...'
    z = zipfile.ZipFile(fn)
    assert len(z.filelist) == 1, 'More than one file in archive?'
    records = [i for i in re.split('\r?\n', z.read(z.filelist[0])) if i]
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    records2 = []
    for row in records:
        r = row.decode(encoding)
        if comp_type == LEGAL_ENTITY:
            pddv = bool(r[0].strip())
            zddv = bool(r[2].strip())
            davcna = r[4:12].strip()
            maticna = r[13:23].strip()
            datum_ddv = r[24:34].strip()
            skd = r[35:41].strip()
            naziv = r[42:142].strip()
            naslov = r[143:256].strip()
            du = r[257:259].strip()
        elif comp_type == SOLE_PROPRIETOR:
            davcna = r[0:8].strip()
            maticna = r[9:19].strip()
            skd = r[20:26].strip()
            naziv = r[27:127].strip()
            naslov = r[128:242].strip()
            du = r[243:].strip()

            pddv = False
            zddv = False
            datum_ddv = ''
        else:
            raise Exception("invalid company type")
        if maticna:
            ulica, hisna, postna, posta = '', '', '', ''
            m = re.match('^(.*?)\s*(\d+)\s*/\s*(\d{4})\s*(.*?)$', naslov)
            if m:
                ulica, hisna, postna, posta = m.groups()
            records2.append({'tax_number': davcna,
                'CompanyNumber': maticna,
                'CompanyName': naziv,
                'RegisteredAddress': naslov,
                'classification': skd,
                'last_seen': today,
                'street_name': ulica,
                'street_number': hisna,
                'zip_code': postna,
                'zip_name': posta,
                'vat_exempt_ZDDV1_76a': pddv,
                'vat_registered': zddv,
                'vat_registered_at': datum_ddv,
                'tax_authority': du,
                'DissolutionDate': '',
                'CompanyType': comp_type,
            })
    print '... done.'
    
    POcheck = [i for i in records2 if i['CompanyNumber'] == "5022762000"]
    FOzDcheck = [i for i in records2 if i['CompanyNumber'] == "3119335000"]

    # check encoding
    assert bool(POcheck) or bool(FOzDcheck), 'Error: missing encoding check entity'
    if POcheck:
        assert POcheck[0]['CompanyName'] == u"OKRO\u017dNO SODI\u0160\u010cE V LJUBLJANI", 'PO.txt encoding error'
    if FOzDcheck:
        assert FOzDcheck[0]['CompanyName'] == u"PROCESNO KRMILJENJE IN RA\u010cUNALNI\u0160TVO EPC JO\u017dEF GERE\u010cNIK S.P.", 'FOzD.txt encoding error'
    return records2

def merge_records(records):
    print 'Saving...'
    import scraperwiki.sqlite
    scraperwiki.sqlite.save(unique_keys=['CompanyNumber'], data=records)
    print 'Marking unseen entities as dissolved...'
    yday = datetime.date.today()
    yyday = yday - datetime.timedelta(1)
    scraperwiki.sqlite.execute('UPDATE swdata SET DissolutionDate = ? WHERE last_seen=?', [yday.strftime('%Y-%m-%d'), yyday.strftime('%Y-%m-%d')])
    scraperwiki.sqlite.commit()
    print '... done.'


# main
# for fn, ty in [(PO_zipurl, LEGAL_ENTITY), (FOzD_zipurl, SOLE_PROPRIETOR)]:
for fn, ty in [(PO_zipurl, LEGAL_ENTITY)]:
    z = get_zip(fn)
    records = get_records(z.name, ty)
    merge_records(records)
    merge_records([])

encoding = 'utf-8'

#PO_zipurl = "http://www.gov.si/aplikacije/durs/PO.zip"
#FOzD_zipurl = "http://www.gov.si/aplikacije/durs/FOzD.zip"


PO_zipurl = "http://datoteke.durs.gov.si/DURS_zavezanci_PO.zip"
FOzD_zipurl = "http://datoteke.durs.gov.si/DURS_zavezanci_DEJ.zip"


LEGAL_ENTITY = "legal entity"
SOLE_PROPRIETOR = 'sole proprietor'

# ========================================
import datetime
import re
import tempfile
import urllib
import zipfile

def get_zip(url):
    print 'Fetching %s ...' % (url,)
    tmp = tempfile.NamedTemporaryFile(suffix='.zip')
    urllib.urlretrieve(url, tmp.name)
    print '... done.'
    return tmp

def get_records(fn, comp_type):
    print 'Parsing file...'
    z = zipfile.ZipFile(fn)
    assert len(z.filelist) == 1, 'More than one file in archive?'
    records = [i for i in re.split('\r?\n', z.read(z.filelist[0])) if i]
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    records2 = []
    for row in records:
        r = row.decode(encoding)
        if comp_type == LEGAL_ENTITY:
            pddv = bool(r[0].strip())
            zddv = bool(r[2].strip())
            davcna = r[4:12].strip()
            maticna = r[13:23].strip()
            datum_ddv = r[24:34].strip()
            skd = r[35:41].strip()
            naziv = r[42:142].strip()
            naslov = r[143:256].strip()
            du = r[257:259].strip()
        elif comp_type == SOLE_PROPRIETOR:
            davcna = r[0:8].strip()
            maticna = r[9:19].strip()
            skd = r[20:26].strip()
            naziv = r[27:127].strip()
            naslov = r[128:242].strip()
            du = r[243:].strip()

            pddv = False
            zddv = False
            datum_ddv = ''
        else:
            raise Exception("invalid company type")
        if maticna:
            ulica, hisna, postna, posta = '', '', '', ''
            m = re.match('^(.*?)\s*(\d+)\s*/\s*(\d{4})\s*(.*?)$', naslov)
            if m:
                ulica, hisna, postna, posta = m.groups()
            records2.append({'tax_number': davcna,
                'CompanyNumber': maticna,
                'CompanyName': naziv,
                'RegisteredAddress': naslov,
                'classification': skd,
                'last_seen': today,
                'street_name': ulica,
                'street_number': hisna,
                'zip_code': postna,
                'zip_name': posta,
                'vat_exempt_ZDDV1_76a': pddv,
                'vat_registered': zddv,
                'vat_registered_at': datum_ddv,
                'tax_authority': du,
                'DissolutionDate': '',
                'CompanyType': comp_type,
            })
    print '... done.'
    
    POcheck = [i for i in records2 if i['CompanyNumber'] == "5022762000"]
    FOzDcheck = [i for i in records2 if i['CompanyNumber'] == "3119335000"]

    # check encoding
    assert bool(POcheck) or bool(FOzDcheck), 'Error: missing encoding check entity'
    if POcheck:
        assert POcheck[0]['CompanyName'] == u"OKRO\u017dNO SODI\u0160\u010cE V LJUBLJANI", 'PO.txt encoding error'
    if FOzDcheck:
        assert FOzDcheck[0]['CompanyName'] == u"PROCESNO KRMILJENJE IN RA\u010cUNALNI\u0160TVO EPC JO\u017dEF GERE\u010cNIK S.P.", 'FOzD.txt encoding error'
    return records2

def merge_records(records):
    print 'Saving...'
    import scraperwiki.sqlite
    scraperwiki.sqlite.save(unique_keys=['CompanyNumber'], data=records)
    print 'Marking unseen entities as dissolved...'
    yday = datetime.date.today()
    yyday = yday - datetime.timedelta(1)
    scraperwiki.sqlite.execute('UPDATE swdata SET DissolutionDate = ? WHERE last_seen=?', [yday.strftime('%Y-%m-%d'), yyday.strftime('%Y-%m-%d')])
    scraperwiki.sqlite.commit()
    print '... done.'


# main
# for fn, ty in [(PO_zipurl, LEGAL_ENTITY), (FOzD_zipurl, SOLE_PROPRIETOR)]:
for fn, ty in [(PO_zipurl, LEGAL_ENTITY)]:
    z = get_zip(fn)
    records = get_records(z.name, ty)
    merge_records(records)
    merge_records([])

