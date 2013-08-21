import urllib
import csv
import scraperwiki


url = "http://farmacias.ath.cx/silo/apps/files_sharing/get.php?token=c849c06c6fc9f1153cefed4175cb806d0b8e3409"

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines,encoding='utf-8', delimiter=';'))

#headers = clist.pop(1)
headers = ['Nome', 'Morada', 'CPostal', 'Telefone', 'Tipo de Prestador', 'URL', 'Mapa', 'E-mail', 'Latitude', 'Longitude']
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist[2:]:
   # print dict(zip(headers, row))
    scraperwiki.sqlite.save(["URL"], dict(zip(headers, row)))