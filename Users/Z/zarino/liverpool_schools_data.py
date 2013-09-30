# Liverpool Schools Data

# Data from Dept for Education (released under Crown Copyright):
# http://www.education.gov.uk/schools/performance/download_data.html
# 
# Data used here in accordance with the DfE's terms:
# http://www.education.gov.uk/help/legalinformation/a005237/use-of-crown-copyright-material


import scraperwiki
import csv


# gives us a pretty screenshot
scraperwiki.scrape('http://www.education.gov.uk/schools/performance/index.html')


# handy variables
base_url  = 'http://www.education.gov.uk/schools/performance/download/csv/'

spine_csv = '341_spine.csv' # school name, id, address, etc
absence_csv = '341_abs.csv'
census_csv = '341_census.csv' # pupil info, eg free school meals, first languages
spend_csv = '341_cfr.csv'
workforce_csv = '341_swf.csv'

spine_meta = 'spine_meta.csv'   # 
absence_meta = 'abs_meta.csv'   # What all the acronyms
census_meta = 'census_meta.csv' # in the other CSVs
spend_meta = 'cfr_meta.csv'     # actually mean
workforce_meta = 'swf_meta.csv' # 


def import_spine():
    rows = scraperwiki.scrape(base_url + spine_csv).splitlines()
    rows = csv.DictReader(rows)
    int_cols = ['URN', 'LA', 'ESTAB', 'LAESTAB', 'ICLOSE', 'ISNEW', 'ISPRIMARY', 'ISSECONDARY', 'ISPOST16', 'AGEL', 'AGEH', 'SFGENDER', 'NEWACFLAG']
    for row in rows:
        for col in int_cols:
            row[col] = int(row[col])
        scraperwiki.sqlite.save(['URN', 'ESTAB'], row, table_name='spine')



def import_absence():
    rows = scraperwiki.scrape(base_url + absence_csv).splitlines()
    rows = csv.DictReader(rows)
    int_cols = ['URN', 'LA', 'ESTAB']
    float_cols = ['PERCTOT', 'PERCUA', 'PPERSABS15', 'PPERSABS20']
    for row in rows:
        if row['URN'].isdigit(): # skip the summary rows at the end
            for col in int_cols:
                row[col] = int(row[col])
            for col in float_cols:
                row[col] = float(row[col])
            scraperwiki.sqlite.save(['URN', 'ESTAB'], row, table_name='absence')



def import_census():
    rows = scraperwiki.scrape(base_url + census_csv).splitlines()
    rows = csv.DictReader(rows)
    int_cols = ['URN', 'LAESTAB']
    for row in rows:
        if row['URN'].isdigit() and row['NUMFTE'].isdigit(): # skip the summary and NP rows at the end
            for col in int_cols:
                row[col] = int(row[col])
            scraperwiki.sqlite.save(['URN', 'LAESTAB'], row, table_name='census')



def import_spend():
    rows = scraperwiki.scrape(base_url + spend_csv).splitlines()
    rows = csv.DictReader(rows)
    int_cols = ['URN', 'LANUMBER']
    for row in rows:
        if row['URN'].isdigit(): # skip the summary rows at the end
            del row['LONDON/NON-LONDON']
            for col in int_cols:
                row[col] = int(row[col])
            scraperwiki.sqlite.save(['URN'], row, table_name='spend')



def import_workforce():
    rows = scraperwiki.scrape(base_url + workforce_csv).splitlines()
    rows = csv.DictReader(rows)
    int_cols = ['URN', 'LA']
    for row in rows:
        if row['URN'].isdigit(): # skip the summary rows at the end
            for col in int_cols:
                row[col] = int(row[col])
            scraperwiki.sqlite.save(['URN'], row, table_name='workforce')



def import_meta():
    rows = scraperwiki.scrape(base_url + spine_meta).splitlines()
    rows = csv.DictReader(rows)
    for row in rows:
        scraperwiki.sqlite.save(['Variable'], row, table_name='spine_meta')
    
    rows = scraperwiki.scrape(base_url + absence_meta).splitlines()
    rows = csv.DictReader(rows)
    for row in rows:
        scraperwiki.sqlite.save(['Variable'], row, table_name='absence_meta')
    
    rows = scraperwiki.scrape(base_url + census_meta).splitlines()
    rows = csv.DictReader(rows)
    for row in rows:
        scraperwiki.sqlite.save(['Variable'], row, table_name='census_meta')
    
    rows = scraperwiki.scrape(base_url + spend_meta).splitlines()
    rows = csv.DictReader(rows)
    for row in rows:
        scraperwiki.sqlite.save(['Variable'], row, table_name='spend_meta')
    
    rows = scraperwiki.scrape(base_url + workforce_meta).splitlines()
    rows = csv.DictReader(rows)
    for row in rows:
        scraperwiki.sqlite.save(['Variable'], row, table_name='workforce_meta')



def geocode_spine():
    rows = scraperwiki.sqlite.select('* FROM spine WHERE lat IS NULL')
    for row in rows:
        loc = scraperwiki.geo.gb_postcode_to_latlng( row['POSTCODE'].replace(' ', '') )
        if loc:
            row['lat'] = loc[0]
            row['long'] = loc[1]
            scraperwiki.sqlite.save(['URN', 'ESTAB'], row, table_name='spine')
        else:
            if row['POSTCODE'] == 'L11 3DQ':
                row['lat'] = 53.446938;
                row['long'] = -2.91574
                scraperwiki.sqlite.save(['URN', 'ESTAB'], row, table_name='spine')
            elif row['POSTCODE'] == 'L8 3TR':
                row['lat'] = 53.389112;
                row['long'] = -2.95934
                scraperwiki.sqlite.save(['URN', 'ESTAB'], row, table_name='spine')



def remove_supp():
    for table in ['census', 'spend', 'workforce']:
        cols = scraperwiki.sqlite.execute('PRAGMA table_info(' + table + ')')
        scraperwiki.sqlite.commit()
        for col in cols['data']:
            scraperwiki.sqlite.execute('UPDATE ' + table + ' SET ' + col[1] + ' = NULL WHERE ' + col[1] + ' = "SUPP"')
            scraperwiki.sqlite.commit()




# Liverpool Schools Data

# Data from Dept for Education (released under Crown Copyright):
# http://www.education.gov.uk/schools/performance/download_data.html
# 
# Data used here in accordance with the DfE's terms:
# http://www.education.gov.uk/help/legalinformation/a005237/use-of-crown-copyright-material


import scraperwiki
import csv


# gives us a pretty screenshot
scraperwiki.scrape('http://www.education.gov.uk/schools/performance/index.html')


# handy variables
base_url  = 'http://www.education.gov.uk/schools/performance/download/csv/'

spine_csv = '341_spine.csv' # school name, id, address, etc
absence_csv = '341_abs.csv'
census_csv = '341_census.csv' # pupil info, eg free school meals, first languages
spend_csv = '341_cfr.csv'
workforce_csv = '341_swf.csv'

spine_meta = 'spine_meta.csv'   # 
absence_meta = 'abs_meta.csv'   # What all the acronyms
census_meta = 'census_meta.csv' # in the other CSVs
spend_meta = 'cfr_meta.csv'     # actually mean
workforce_meta = 'swf_meta.csv' # 


def import_spine():
    rows = scraperwiki.scrape(base_url + spine_csv).splitlines()
    rows = csv.DictReader(rows)
    int_cols = ['URN', 'LA', 'ESTAB', 'LAESTAB', 'ICLOSE', 'ISNEW', 'ISPRIMARY', 'ISSECONDARY', 'ISPOST16', 'AGEL', 'AGEH', 'SFGENDER', 'NEWACFLAG']
    for row in rows:
        for col in int_cols:
            row[col] = int(row[col])
        scraperwiki.sqlite.save(['URN', 'ESTAB'], row, table_name='spine')



def import_absence():
    rows = scraperwiki.scrape(base_url + absence_csv).splitlines()
    rows = csv.DictReader(rows)
    int_cols = ['URN', 'LA', 'ESTAB']
    float_cols = ['PERCTOT', 'PERCUA', 'PPERSABS15', 'PPERSABS20']
    for row in rows:
        if row['URN'].isdigit(): # skip the summary rows at the end
            for col in int_cols:
                row[col] = int(row[col])
            for col in float_cols:
                row[col] = float(row[col])
            scraperwiki.sqlite.save(['URN', 'ESTAB'], row, table_name='absence')



def import_census():
    rows = scraperwiki.scrape(base_url + census_csv).splitlines()
    rows = csv.DictReader(rows)
    int_cols = ['URN', 'LAESTAB']
    for row in rows:
        if row['URN'].isdigit() and row['NUMFTE'].isdigit(): # skip the summary and NP rows at the end
            for col in int_cols:
                row[col] = int(row[col])
            scraperwiki.sqlite.save(['URN', 'LAESTAB'], row, table_name='census')



def import_spend():
    rows = scraperwiki.scrape(base_url + spend_csv).splitlines()
    rows = csv.DictReader(rows)
    int_cols = ['URN', 'LANUMBER']
    for row in rows:
        if row['URN'].isdigit(): # skip the summary rows at the end
            del row['LONDON/NON-LONDON']
            for col in int_cols:
                row[col] = int(row[col])
            scraperwiki.sqlite.save(['URN'], row, table_name='spend')



def import_workforce():
    rows = scraperwiki.scrape(base_url + workforce_csv).splitlines()
    rows = csv.DictReader(rows)
    int_cols = ['URN', 'LA']
    for row in rows:
        if row['URN'].isdigit(): # skip the summary rows at the end
            for col in int_cols:
                row[col] = int(row[col])
            scraperwiki.sqlite.save(['URN'], row, table_name='workforce')



def import_meta():
    rows = scraperwiki.scrape(base_url + spine_meta).splitlines()
    rows = csv.DictReader(rows)
    for row in rows:
        scraperwiki.sqlite.save(['Variable'], row, table_name='spine_meta')
    
    rows = scraperwiki.scrape(base_url + absence_meta).splitlines()
    rows = csv.DictReader(rows)
    for row in rows:
        scraperwiki.sqlite.save(['Variable'], row, table_name='absence_meta')
    
    rows = scraperwiki.scrape(base_url + census_meta).splitlines()
    rows = csv.DictReader(rows)
    for row in rows:
        scraperwiki.sqlite.save(['Variable'], row, table_name='census_meta')
    
    rows = scraperwiki.scrape(base_url + spend_meta).splitlines()
    rows = csv.DictReader(rows)
    for row in rows:
        scraperwiki.sqlite.save(['Variable'], row, table_name='spend_meta')
    
    rows = scraperwiki.scrape(base_url + workforce_meta).splitlines()
    rows = csv.DictReader(rows)
    for row in rows:
        scraperwiki.sqlite.save(['Variable'], row, table_name='workforce_meta')



def geocode_spine():
    rows = scraperwiki.sqlite.select('* FROM spine WHERE lat IS NULL')
    for row in rows:
        loc = scraperwiki.geo.gb_postcode_to_latlng( row['POSTCODE'].replace(' ', '') )
        if loc:
            row['lat'] = loc[0]
            row['long'] = loc[1]
            scraperwiki.sqlite.save(['URN', 'ESTAB'], row, table_name='spine')
        else:
            if row['POSTCODE'] == 'L11 3DQ':
                row['lat'] = 53.446938;
                row['long'] = -2.91574
                scraperwiki.sqlite.save(['URN', 'ESTAB'], row, table_name='spine')
            elif row['POSTCODE'] == 'L8 3TR':
                row['lat'] = 53.389112;
                row['long'] = -2.95934
                scraperwiki.sqlite.save(['URN', 'ESTAB'], row, table_name='spine')



def remove_supp():
    for table in ['census', 'spend', 'workforce']:
        cols = scraperwiki.sqlite.execute('PRAGMA table_info(' + table + ')')
        scraperwiki.sqlite.commit()
        for col in cols['data']:
            scraperwiki.sqlite.execute('UPDATE ' + table + ' SET ' + col[1] + ' = NULL WHERE ' + col[1] + ' = "SUPP"')
            scraperwiki.sqlite.commit()




