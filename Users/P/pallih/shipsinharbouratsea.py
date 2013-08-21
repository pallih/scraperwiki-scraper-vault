import scraperwiki
import requests
from lxml import etree
import lxml.html
import datetime

last_run = datetime.datetime.now()

ships_in_port_url = 'http://www.112.is/Stat/StatsService.asmx/ShipInPortInSea'

post_data = {"Content-Length": 0}
r = requests.post(ships_in_port_url, post_data)
xml = r.content.encode('utf-8')
ships = {}
parser = etree.XMLParser()
tree = etree.XML(xml, parser)
for node in tree.iter('{http://tempuri.org/}ShipInPortInSea'):
    for item in node.iter('{http://tempuri.org/}CurrDate'):
        ships['Date'] = item.text #, item.nsmap
    for item in node.iter('{http://tempuri.org/}HourFrom'):
        ships['Hour from'] = item.text
    for item in node.iter('{http://tempuri.org/}HourTo'):
        ships['Hour to'] = item.text
    for item in node.iter('{http://tempuri.org/}Sea'):
        ships['At sea'] = item.text
    for item in node.iter('{http://tempuri.org/}Port'):
        ships['NOT at sea'] = item.text
print ships
           




