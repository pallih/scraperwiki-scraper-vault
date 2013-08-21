import scraperwiki
import requests
from BeautifulSoup import BeautifulSoup

resp = requests.get('http://trends.google.com/websites?q=breitbart.com')
soup = BeautifulSoup(resp.text)

print soup.prettify()

tables = soup.findAll('table')
print "Found {0} tables".format(len(tables))

third_table = tables[-1]
if third_table:
    # print third_table
    print type(third_table)
    barchart_name_list = third_table.findAll('td', {'class':'trends-barchart-name-cell'})
    barchart_names = [el.text for el in barchart_name_list]
    print barchart_names