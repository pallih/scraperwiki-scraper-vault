import scraperwiki
import lxml.etree
import lxml.html


root = lxml.html.parse(r'http://pe.usps.gov/text/pub28/pub28apc_002.htm').getroot()


for tr in root.cssselect('table #ep533076 tr'):
    a = tr.cssselect('td p a')
    if len(a) >1:
        data = { 'full' : a[0].text,
                 'abbr' : a[-1].text
        }

        if data['full'] == 'BAYOU': data['abbr'] = 'BYU'
        if data['full'] == 'Primary': continue

        scraperwiki.sqlite.save(unique_keys=['full'], data=data)