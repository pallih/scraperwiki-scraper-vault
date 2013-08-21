import scraperwiki
import requests
# from lxml import etree
import lxml.html
import datetime

now = datetime.datetime.now()

#print "Hour: %d" % now.hour

ships_in_port_url = 'http://www.112.is/Stat/StatsService.asmx/RepPolice'

post_data = {"Content-Length": 0}

r = requests.post(ships_in_port_url, post_data)

xml = r.content.encode('utf-8')

#print xml

#root = etree.fromstring(xml)
root = lxml.html.fromstring(xml)
nodes = root.xpath('//arrayofreppolice/reppolice')
for m in nodes[23:]:
    record = {}
    for d in m:
        record[d.tag] = d.text
    print '<br><br><br><br><br><br><br><br><br><br><br><br><p style="color:sienna;text-align:center;font-size:40pt;vertical-align:middle">Síðasta klukkutímann hefur lögreglan sinnt <font size="40pt" color="black">', record['police'], '</font> útköllum frá 112</p></div>'

            


