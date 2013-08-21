import scraperwiki
from bs4 import BeautifulSoup
import requests
import csv

url = "http://www.crimemapping.com/DetailedReport.aspx?db=3/24/2012+00:00:00&de=3/30/2012+23:59:00&ccs=AR,AS,BU,DP,DR,DU,FR,HO,VT,RO,SX,TH,VA,VB,WE&xmin=-8569278.80402062&ymin=4412938.95382204&xmax=-8414723.132827936&ymax=4457272.4302274585&faid=cd940d74-f697-4cd2-bd08-fb0615a89be9"
r = requests.get(url)
soup = BeautifulSoup(r.text)
table = soup.findAll('table')[0]
crimelist = []
for row in table.findAll('tr')[1:]:
    if row.text.strip()=='':
        pass
    else:
        cells = row.findAll('td')[1:]
        entry = [cell.text for cell in cells]
        crimelist.append(entry)

print crimelist

for FinalCrime in crimelist:
    scraperwiki.sqlite.save(["ID"[1]],FinalCrime, table_name='Norfolkcrime')

# then you could output to csv, like this:

#header = ['Incident', 'ID', 'Address', 'Agency', 'Datetime']
#outfile = "[PATH TO YOUR CSV FILE]"
#with open(outfile, 'wb') as f:
#    cWriter=csv.writer(f)
#    cWriter.writerow(header)
#    for line in crimelist:
#        cWriter.writerow(line)

