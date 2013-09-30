sourcescraper = 'congreso_datos_diputado'

import json
import urllib2
headers = { 'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.6.0' }

JSON_URL = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=json&name=congreso_datos_diputado&query=select+*+from+%60swdata%60&apikey='

req = urllib2.Request(JSON_URL, None, headers)
fp = urllib2.urlopen(req)
diputadosdata = json.load(fp)
fp.close()

sin_dec_bienes = []
sin_dec_activ = []

print '<p>CON declaración de bienes</p>'
print '<ul>'
for diputado in diputadosdata:
    dec_url = diputado.get('declaracion_bienes_url')
    if dec_url:
        print '<li><a href="%s">%s %s</a></li>' %(dec_url, diputado.get('nombre'), diputado.get('apellidos'))
    else:
        sin_dec_bienes.append(diputado)

print '</ul>'
print '<br><br>'
print '<p>SIN declaracion de bienes (TOTAL: %d)</p>' %len(sin_dec_bienes)

for diputado in sin_dec_bienes:
    print '%s %s<br>' %(diputado.get('nombre'), diputado.get('apellidos'))


print '<p>CON declaración de actividades</p>'
print '<ul>'
for diputado in diputadosdata:
    dec_url = diputado.get('declaracion_actividades_url')
    if dec_url:
        print '<li><a href="%s">%s %s</a></li>' %(dec_url, diputado.get('nombre'), diputado.get('apellidos'))
    else:
        sin_dec_activ.append(diputado)

print '</ul>'
print '<br><br>'
print '<p>SIN declaracion de actividades (TOTAL: %d)</p>' %len(sin_dec_activ)

for diputado in sin_dec_activ:
    print '%s %s<br>' %(diputado.get('nombre'), diputado.get('apellidos'))
print '<br><br>FIN'
sourcescraper = 'congreso_datos_diputado'

import json
import urllib2
headers = { 'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.6.0' }

JSON_URL = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=json&name=congreso_datos_diputado&query=select+*+from+%60swdata%60&apikey='

req = urllib2.Request(JSON_URL, None, headers)
fp = urllib2.urlopen(req)
diputadosdata = json.load(fp)
fp.close()

sin_dec_bienes = []
sin_dec_activ = []

print '<p>CON declaración de bienes</p>'
print '<ul>'
for diputado in diputadosdata:
    dec_url = diputado.get('declaracion_bienes_url')
    if dec_url:
        print '<li><a href="%s">%s %s</a></li>' %(dec_url, diputado.get('nombre'), diputado.get('apellidos'))
    else:
        sin_dec_bienes.append(diputado)

print '</ul>'
print '<br><br>'
print '<p>SIN declaracion de bienes (TOTAL: %d)</p>' %len(sin_dec_bienes)

for diputado in sin_dec_bienes:
    print '%s %s<br>' %(diputado.get('nombre'), diputado.get('apellidos'))


print '<p>CON declaración de actividades</p>'
print '<ul>'
for diputado in diputadosdata:
    dec_url = diputado.get('declaracion_actividades_url')
    if dec_url:
        print '<li><a href="%s">%s %s</a></li>' %(dec_url, diputado.get('nombre'), diputado.get('apellidos'))
    else:
        sin_dec_activ.append(diputado)

print '</ul>'
print '<br><br>'
print '<p>SIN declaracion de actividades (TOTAL: %d)</p>' %len(sin_dec_activ)

for diputado in sin_dec_activ:
    print '%s %s<br>' %(diputado.get('nombre'), diputado.get('apellidos'))
print '<br><br>FIN'
