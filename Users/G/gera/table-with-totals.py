import scraperwiki

sourcescraper = "censo-2010-argentina"
 
limit = 20
offset = 0

print '<h2>Totales del Censo Argentina 2010</h2>'
print '<table border="1" style="border-collapse:collapse;">'

provincias = {}

prov = 'provincia'
fem  = 'total_mujeres'
masc = 'total_varones'
viv  = 'total_viviendas'

keys = (prov, fem, masc, viv)
template = {}.fromkeys(keys, 0)
totals = template.copy()
 
scraperwiki.sqlite.attach(sourcescraper)

# compute totals
for row in scraperwiki.sqlite.select('* from `%s`.swdata' % sourcescraper): #getData(sourcescraper): #, limit, offset):
    nombre = row.get(prov)
    p = provincias.get(nombre, template.copy())
    p[prov] = nombre
    p[fem]  += long(row.get(fem))
    p[masc] += long(row.get(masc))
    p[viv]  += long(row.get(viv))
    provincias[nombre] = p

# column headings
print "<tr>",
for key in keys:
    print "<th>%s</th>" % key.replace('_',' '),
print "</tr>"

# column data
# compute big total
for provincia in provincias.itervalues():
    print "<tr>",
    for key in keys:
        value = provincia[key]
        if key != prov:
            totals[key] += value
        print "<td>%s</td>" % value,
    print "</tr>"

totals[prov] = 'totales'
print "<tr>",
for key in keys:
    print "<th>%s</th>" % totals[key],
print "</tr>"
 
print "</table>"

import scraperwiki

sourcescraper = "censo-2010-argentina"
 
limit = 20
offset = 0

print '<h2>Totales del Censo Argentina 2010</h2>'
print '<table border="1" style="border-collapse:collapse;">'

provincias = {}

prov = 'provincia'
fem  = 'total_mujeres'
masc = 'total_varones'
viv  = 'total_viviendas'

keys = (prov, fem, masc, viv)
template = {}.fromkeys(keys, 0)
totals = template.copy()
 
scraperwiki.sqlite.attach(sourcescraper)

# compute totals
for row in scraperwiki.sqlite.select('* from `%s`.swdata' % sourcescraper): #getData(sourcescraper): #, limit, offset):
    nombre = row.get(prov)
    p = provincias.get(nombre, template.copy())
    p[prov] = nombre
    p[fem]  += long(row.get(fem))
    p[masc] += long(row.get(masc))
    p[viv]  += long(row.get(viv))
    provincias[nombre] = p

# column headings
print "<tr>",
for key in keys:
    print "<th>%s</th>" % key.replace('_',' '),
print "</tr>"

# column data
# compute big total
for provincia in provincias.itervalues():
    print "<tr>",
    for key in keys:
        value = provincia[key]
        if key != prov:
            totals[key] += value
        print "<td>%s</td>" % value,
    print "</tr>"

totals[prov] = 'totales'
print "<tr>",
for key in keys:
    print "<th>%s</th>" % totals[key],
print "</tr>"
 
print "</table>"

