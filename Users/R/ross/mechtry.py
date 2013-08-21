import re
import mechanize
import scraperwiki
from lxml.html import fromstring

root = "http://cgrw01.cgr.go.cr/apex/f?p=307:36:0::NO::P36_W_ANIO,P36_W_SUBPARTIDA,P36_W_DESCR_SUBPARTIDA,P36_TOT_MONTO_ADJUD_COL:2013,1.01.01,%5CAlquiler%20de%20edificios,%20locales%20y%20terrenos%5C,%5C122830687079,19%5C"


br = mechanize.Browser()
response = br.open(root)

content = response.read()
while True:
    page = fromstring(content)
    #process_content

    print page.cssselect('.pagination span a')[0]
    #click next if exists else break

    break