# 195 50 15

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

url= 'http://www.camskill.co.uk/products.php?plid=m53b0s99p0'
html = scraperwiki.scrape(url)

soup = BeautifulSoup(html)

Range0to19 = 0
Range20to29 = 0
Range30to39 = 0
Range40to49 = 0
Range50to59 = 0
Range60to69 = 0
Range70to79 = 0
Range80to89 = 0
Range90to99 = 0
Range100Above = 0

tds = soup.findAll('td') 
for td in tds:

    ProdID = '-1'
    ProdName = '-1'
    ProdPrice = '-1'

    inputs = td.findAll('input')

    for input in inputs :
        if input['name'] == 'productName':
            ProdName = input['value']
        if input['name'] == 'productPrice':
            ProdPrice = input['value']
        if input['name'] == 'productID':
            ProdID = input['value']

    if ProdName != '-1' :
        if ProdPrice != '-1' :
            if ProdID != '-1' :
                record = { "row" : ProdID + ', ' + ProdName + ', ' + ProdPrice} # column name and value
                
                if float(ProdPrice) >= 100:
                    Range100Above = Range100Above  + 1
                elif float(ProdPrice) >= 90:
                    Range90to99 = Range90to99 + 1
                elif float(ProdPrice) >= 80:
                    Range80to89 = Range80to89 + 1
                elif float(ProdPrice) >= 70:
                    Range70to79 = Range70to79 + 1
                elif float(ProdPrice) >= 60:
                    Range60to69 = Range60to69 + 1
                elif float(ProdPrice) >= 50:
                    Range50to59 = Range50to59 + 1
                elif float(ProdPrice) >= 40:
                    Range40to49 = Range40to49 + 1
                elif float(ProdPrice) >= 30:
                    Range30to39 = Range30to39 + 1
                elif float(ProdPrice) >= 20:
                    Range20to29 = Range20to29 + 1
                else:
                    Range0to19 = Range0to19 + 1
                
ChartURL = "http://chart.apis.google.com/chart?chs=300x225&cht=p&chd=s:mwtv726mjg&chco=FF0000|008000|0000FF|FF9900|000000|990066|00FF00|F607A7|FFCC00|3399CC&"
ChartURL = ChartURL + "chd=t:" + str(Range0to19) + "," + str(Range20to29) + "," + str(Range30to39) + "," + str(Range40to49) + "," + str(Range50to59) + "," + str(Range60to69) + "," + str(Range70to79) + "," + str(Range80to89) + "," + str(Range90to99) + "," + str(Range100Above) + "&"
ChartURL = ChartURL + "chdl=%C2%A30+to+%C2%A319|%C2%A320+to+%C2%A329|%C2%A330+to+%C2%A339|%C2%A340+to+%C2%A349|%C2%A350+to+%C2%A359|%C2%A360+to+%C2%A369|%C2%A370+to+%C2%A379|%C2%A380+to+%C2%A389|%C2%A390+to+%C2%A399|%C2%A3100+%2B'"
print "<img src='" + ChartURL + "width='300' height='225' alt='' />"
            

