import scraperwiki

postcodes = ['M14 6','M20 2','PR9 9','M33 3','M16 8','CH5 4','M15 4','WA2 0','CH3 5','WA4 2','CW9 8','M21 9','CH7 6','CH66 2','WA11 0','WN6 0','M33 2','SK8 3','M33 4','PR8 3','WN2 4','BL5 3','PR8 6','WA9 4','SK4 4','WN3 6','WA8 9','M29 7','WN8 6','M20 4￼￼￼￼￼￼','CH2 3','WN5 7','PR5 4','CH6 5','PR9 7','M20 6','PR8 2','CW8 2','WA15 6','PR9 0','WA5 1','PR8 4','PR7 5','CH5 3','PR4 6','M24 1','WA7 6','BL3 4','BL5 2','WA15 7']

data = []

#for postcode in postcodes:
#    data.append({'postcode': postcode})

#scraperwiki.sqlite.save(['postcode'], data)

rows = scraperwiki.sqlite.select('* from swdata where lat is null')

scraperwiki.sqlite.attach('uk_postcodes_from_codepoint', 'p')

for row in rows:
    lres = scraperwiki.sqlite.select('Northings, Eastings from p.swdata where Postcode like "' + row['postcode'].replace(' ', '') + '%" limit 1')
    if lres:
        loc = scraperwiki.geo.os_easting_northing_to_latlng(lres[0]['Eastings'], lres[0]['Northings'], grid='GB')
        row['lat'] = loc[0]
        row['long'] = loc[1]
        print '-- geocoded ' + row['postcode']
        scraperwiki.sqlite.save(['postcode'], row)import scraperwiki

postcodes = ['M14 6','M20 2','PR9 9','M33 3','M16 8','CH5 4','M15 4','WA2 0','CH3 5','WA4 2','CW9 8','M21 9','CH7 6','CH66 2','WA11 0','WN6 0','M33 2','SK8 3','M33 4','PR8 3','WN2 4','BL5 3','PR8 6','WA9 4','SK4 4','WN3 6','WA8 9','M29 7','WN8 6','M20 4￼￼￼￼￼￼','CH2 3','WN5 7','PR5 4','CH6 5','PR9 7','M20 6','PR8 2','CW8 2','WA15 6','PR9 0','WA5 1','PR8 4','PR7 5','CH5 3','PR4 6','M24 1','WA7 6','BL3 4','BL5 2','WA15 7']

data = []

#for postcode in postcodes:
#    data.append({'postcode': postcode})

#scraperwiki.sqlite.save(['postcode'], data)

rows = scraperwiki.sqlite.select('* from swdata where lat is null')

scraperwiki.sqlite.attach('uk_postcodes_from_codepoint', 'p')

for row in rows:
    lres = scraperwiki.sqlite.select('Northings, Eastings from p.swdata where Postcode like "' + row['postcode'].replace(' ', '') + '%" limit 1')
    if lres:
        loc = scraperwiki.geo.os_easting_northing_to_latlng(lres[0]['Eastings'], lres[0]['Northings'], grid='GB')
        row['lat'] = loc[0]
        row['long'] = loc[1]
        print '-- geocoded ' + row['postcode']
        scraperwiki.sqlite.save(['postcode'], row)