# Scraping Indices of Deprivation 2010
# LSOA data from data.gov.uk and the Department for Communities and Local Government

from __future__ import division
import scraperwiki
import tempfile
import csv


def main():
    # get pretty screenshot
    scraperwiki.scrape('http://www.communities.gov.uk/publications/corporate/statistics/indices2010')
    extract_data_from_csv_2()



def extract_data_from_csv_2():
    print 'Downloading file from communities.gov.uk...'
    f = scraperwiki.scrape('http://www.communities.gov.uk/documents/statistics/xls/1871702.csv')

    print 'Reading csv file'
    reader = csv.reader(f.splitlines())
    rows = list(reader)

    print 'Getting column headers'
    headers = []
    sqlite_cols = []
    for header in rows[0]:
        # convert row header into something shorter and safer
        safe = header.lower().replace(' ', '_').replace('/', '_').replace('_(where_1_is_most_deprived)','')
        # work out what type of content that column will hold
        if safe.startswith('rank'):
            col_type = 'INTEGER'
        elif safe.endswith('score'):
            col_type = 'FLOAT'
        else:
            col_type = 'TEXT'
        if safe=='lsoa_code':
            col_type += ' UNIQUE'
        sqlite_cols.append('`%s` %s' % (safe, col_type))
        headers.append(safe)

    print 'Creating sqlite table'
    scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `imd_2010` (' + ', '.join(sqlite_cols) + ')')
    scraperwiki.sqlite.execute('CREATE UNIQUE INDEX IF NOT EXISTS lsoa_code_index ON imd_2010 (lsoa_code)')
    scraperwiki.sqlite.commit()
    
    print 'Extracting data'
    data = []
    for row_number in range(1, len(rows)):
        temp = {}
        for cell_number in range(0, len(rows[row_number])):
            temp[headers[cell_number]] = rows[row_number][cell_number]
        data.append(temp)
        if row_number > 1 and row_number%500==1:
            scraperwiki.sqlite.save([], data, 'imd_2010')
            data = []
            print '-- ' + str(round(row_number/len(rows)*100, 1)) + '% done'
    if data:
        scraperwiki.sqlite.save([], data, 'imd_2010')

    print '-- All done!'


main()




# Scraping Indices of Deprivation 2010
# LSOA data from data.gov.uk and the Department for Communities and Local Government

from __future__ import division
import scraperwiki
import tempfile
import csv


def main():
    # get pretty screenshot
    scraperwiki.scrape('http://www.communities.gov.uk/publications/corporate/statistics/indices2010')
    extract_data_from_csv_2()



def extract_data_from_csv_2():
    print 'Downloading file from communities.gov.uk...'
    f = scraperwiki.scrape('http://www.communities.gov.uk/documents/statistics/xls/1871702.csv')

    print 'Reading csv file'
    reader = csv.reader(f.splitlines())
    rows = list(reader)

    print 'Getting column headers'
    headers = []
    sqlite_cols = []
    for header in rows[0]:
        # convert row header into something shorter and safer
        safe = header.lower().replace(' ', '_').replace('/', '_').replace('_(where_1_is_most_deprived)','')
        # work out what type of content that column will hold
        if safe.startswith('rank'):
            col_type = 'INTEGER'
        elif safe.endswith('score'):
            col_type = 'FLOAT'
        else:
            col_type = 'TEXT'
        if safe=='lsoa_code':
            col_type += ' UNIQUE'
        sqlite_cols.append('`%s` %s' % (safe, col_type))
        headers.append(safe)

    print 'Creating sqlite table'
    scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `imd_2010` (' + ', '.join(sqlite_cols) + ')')
    scraperwiki.sqlite.execute('CREATE UNIQUE INDEX IF NOT EXISTS lsoa_code_index ON imd_2010 (lsoa_code)')
    scraperwiki.sqlite.commit()
    
    print 'Extracting data'
    data = []
    for row_number in range(1, len(rows)):
        temp = {}
        for cell_number in range(0, len(rows[row_number])):
            temp[headers[cell_number]] = rows[row_number][cell_number]
        data.append(temp)
        if row_number > 1 and row_number%500==1:
            scraperwiki.sqlite.save([], data, 'imd_2010')
            data = []
            print '-- ' + str(round(row_number/len(rows)*100, 1)) + '% done'
    if data:
        scraperwiki.sqlite.save([], data, 'imd_2010')

    print '-- All done!'


main()




