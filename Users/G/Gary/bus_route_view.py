import scraperwiki
import re

scraperwiki.sqlite.attach('bus_route') 

blocks = scraperwiki.sqlite.select('* from `bus_route`.swdata')

print '<style type="text/css">'
print 'div #scraperwikipane { display:none; background:none; border:none; top:-300px; }'
print 'a #scraperwikipane { display:none; }'
print '</style>'

print '<table style="border:1px solid silver; padding:0px;">'

for block in blocks:
    route = '<tr style="border:1px solid silver; "><td style="border:1px solid silver; "><div style="margin:2px 4px 2px 4px;">' + block['Time'] + '</div></td><td style="border:1px solid silver; "><div style="margin:2px 4px 2px 4px;">' + block['Destination'] + '</div></td></tr>'
    
    route.lstrip()
    
    print route

print '</table>'import scraperwiki
import re

scraperwiki.sqlite.attach('bus_route') 

blocks = scraperwiki.sqlite.select('* from `bus_route`.swdata')

print '<style type="text/css">'
print 'div #scraperwikipane { display:none; background:none; border:none; top:-300px; }'
print 'a #scraperwikipane { display:none; }'
print '</style>'

print '<table style="border:1px solid silver; padding:0px;">'

for block in blocks:
    route = '<tr style="border:1px solid silver; "><td style="border:1px solid silver; "><div style="margin:2px 4px 2px 4px;">' + block['Time'] + '</div></td><td style="border:1px solid silver; "><div style="margin:2px 4px 2px 4px;">' + block['Destination'] + '</div></td></tr>'
    
    route.lstrip()
    
    print route

print '</table>'