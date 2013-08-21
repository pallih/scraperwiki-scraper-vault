import scraperwiki

def load():
    index = [u'shipment_year', u'taxon_family']
    data = scraperwiki.swimport('csv2sw').read.csv('http://hacks.thomaslevine.com/top10.csv')
    for row in data:
        del(row[''])
    
    scraperwiki.sqlite.save(index, data, 't')

def add_empty_rows():
    for row in scraperwiki.sqlite.select('distinct taxon_family, export_country_code from t'):
        for year in range(1975, 2009):
            scraperwiki.sqlite.save([], {'taxon_family': row['taxon_family'], 'year': year, 'export': 0, 'export_country_code': row['export_country_code']}, 't')


load()
add_empty_rows()
load()