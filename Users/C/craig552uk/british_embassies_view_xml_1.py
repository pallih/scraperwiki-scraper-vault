import scraperwiki

scraperwiki.sqlite.attach("british_embassies")
embassies = scraperwiki.sqlite.select("* from british_embassies.swdata")

scraperwiki.utils.httpresponseheader("Content-Type", "application/xml")

cdata = ['address', 'office_hours']

xml  = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
xml += '<embassies>\n'

for embassy in embassies:
    xml += '  <embassy id="%s">\n' % embassy['url']
    xml += '    <name>%s</name>\n' % embassy['name']
    xml += '    <longitude>%s</longitude>\n' % embassy['longitude']
    xml += '    <latitude>%s</latitude>\n' % embassy['latitude']
    xml += '    <phone>%s</phone>\n' % embassy['phone'].replace('<br>', '')
    xml += '    <email>%s</email>\n' % embassy['email']
    if embassy['web'].startswith('http'):
        xml += '    <url>%s</url>\n' % embassy['web']
    xml += '    <address><![CDATA[%s]]></address>\n' % embassy['address'].replace('</br>', '')
    xml += '    <office_hours><![CDATA[%s]]></office_hours>\n' % embassy['office_hours']
    xml += '  </embassy>\n'

xml += '</embassies>'

print xml