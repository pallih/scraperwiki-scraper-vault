import scraperwiki
import requests
import openpyxl
import tempfile
import time
import pprint

def getworkbook(url):
    # Loads an xlsx file from the internet
    raw = requests.get(url, verify=False).content
    f = tempfile.NamedTemporaryFile('wb')
    f.write(raw)
    f.seek(0)
    wb = openpyxl.load_workbook(f.name)
    f.close()
    return wb

def getdata(wb, sheet='Sheet1'):
    #Turn a sheet on a workbook into an array
    data = wb.get_sheet_by_name(sheet)
    return [[unicode(cell.value).strip() for cell in row] for row in data.rows]

def import_data():
    wb = getworkbook('https://dl.dropbox.com/s/q6enhwmeogbhpfx/corresponding_local_authorities.xlsx?dl=1')
    
    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS `local_authorities`')
    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS `relationships`')
    scraperwiki.sqlite.execute('CREATE TABLE `local_authorities` (`la_code` text primary key, `la_name` text, `country` text)')
    scraperwiki.sqlite.execute('CREATE TABLE `relationships` (`from_la_code` text, `to_la_code` text, `difference` float)')
    scraperwiki.sqlite.commit()

    rows = getdata(wb, 'Corresponding local authorities')
    pprint.pprint(rows)

    local_authorities = []
    relationships = []

    for i in range(15,395):
        if ',' in rows[i][1]:
            print 'skipped entire row for', rows[i][2]
            continue
        else:
            local_authorities.append({
                'la_code': rows[i][1],
                'la_name': rows[i][2],
                'country': rows[i][3]
            })
        for n in [5,9,13,17,21]:
            if ',' in rows[i][n]:
                print 'skipped relationship between', rows[i][2], 'and', rows[i][n+1]
            else:
                relationships.append({
                    'from_la_code': rows[i][1],
                    'to_la_code': rows[i][n],
                    'difference': float(rows[i][n+2])
                })

    scraperwiki.sqlite.save(['la_code'], local_authorities, 'local_authorities')
    scraperwiki.sqlite.save(['from_la_code','to_la_code'], relationships, 'relationships')

import_data()