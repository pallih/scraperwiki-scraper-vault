# Blank Python
#http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.villedraguignan.com%2Fonenparle%2Fagendaloisirs%3Ffilter_by_type_value%3DTous%26amp%3Boption%3Dcom_evenement%26amp%3Bcontroller%3Devenement%26amp%3Btask%3DlistEvents%26amp%3Bdate%3Dmois%26amp%3Blimit%3D0%26amp%3Blimitstart%3D0%22%20and%0A%20%20%20%20%20%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22liste%22%5D%2F%2Ful%2Fli%2Fp%2Fa'&diagnostics=true

#select centroid.latitude, centroid.longitude from geo.places where text="83300 Draguignan"
import scraperwiki
import urllib
import lxml.etree
import lxml.html.clean
#from lxml.html.clean import clean_html #http://codespeak.net/lxml/lxmlhtml.html#cleaning-up-html
from datetime import datetime
import csv

url = "https://spreadsheets.google.com/spreadsheet/pub?hl=fr&hl=fr&key=0AmwtCKEN_vuwdElCajhHMzdGZHAtdElhdWRRaFFQTlE&single=true&gid=0&output=csv"
scraperwiki.sqlite.save_var('data_columns', ['VILLE','CP','AGENDA','SOURCE','LAT','LNG'])
f = urllib.urlopen(url)
lines = f.readlines()
clist = list(csv.reader(lines))
header = clist.pop(0)   # set 'header' to be the first row of the CSV file
for row in clist :
    ville = dict(zip(header, row))
    if 'NOM' in ville.keys() :
        #print ville['LAT'],ville['LNG']
        jscallback = scraperwiki.scrape(ville['SCRAP_SOURCE'])
        pos1 = jscallback.find('"results":["')+12
        pos2 = jscallback.find('"]});')
        strhtml=jscallback[pos1:pos2]
        cleaner = lxml.html.clean.Cleaner(links=False)
        print cleaner.clean_html(strhtml)
        scraperwiki.sqlite.save(unique_keys=["VILLE"], data={"VILLE":ville['NOM'], "CP":ville['CP'],"AGENDA":jscallback,"SOURCE":ville['SOURCE'],"date":datetime.now(),"latlng":(float(ville['LAT']),float(ville['LNG']))})