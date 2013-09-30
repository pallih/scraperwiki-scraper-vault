import scraperwiki
import re

scraperwiki.sqlite.attach('dabs_routers') 

blocks = scraperwiki.sqlite.select('* from `dabs_routers`.swdata')

print '<style type="text/css">'
print 'div #scraperwikipane { display:none; background:none; border:none; top:-300px; }'
print 'a #scraperwikipane { display:none; }'
print '</style>'

print '<table width="504px" style="background-color:black;">'

for block in blocks:
    routerimage = '<a style="float:left; margin-left:85px; margin-top:20px;" target="_blank" title="View ' + block['Name'] + ' on Dabs.com" href="http://www.dabs.com/search?q=' + block['Name'] + '"><img height="80px" border="none" src="http://www.dabs.com/images/product' + block['Image'] + '" /></a>'
    routername = '<div style="height:30px;"></div><a style="color:darkred; text-decoration:none; font-weight:bold;" target="_blank" title="View ' + block['Name'] + ' on Dabs.com" href="http://www.dabs.com/search?q=' + block['Name'] + '">' + block['Name'] + '</a>'
    routerprice = '<p style="float:right; margin-right:85px; font-size:36; color:maroon;">' + block['Price'] + '</p>'
    
    routerimage.lstrip()
    routername.lstrip()
    routerprice.lstrip()
    
    print '<tr><td style="text-align:center;"><div style="height:190px; background-image:url(' + "'" + 'http://www.fibrenet-project.org.uk/wp-content/uploads/2011/11/Trials-link-boxes-2.png' + "'" + ');">', routername, '</br>', routerimage, routerprice, '</div></td></tr>'

print '</table>'import scraperwiki
import re

scraperwiki.sqlite.attach('dabs_routers') 

blocks = scraperwiki.sqlite.select('* from `dabs_routers`.swdata')

print '<style type="text/css">'
print 'div #scraperwikipane { display:none; background:none; border:none; top:-300px; }'
print 'a #scraperwikipane { display:none; }'
print '</style>'

print '<table width="504px" style="background-color:black;">'

for block in blocks:
    routerimage = '<a style="float:left; margin-left:85px; margin-top:20px;" target="_blank" title="View ' + block['Name'] + ' on Dabs.com" href="http://www.dabs.com/search?q=' + block['Name'] + '"><img height="80px" border="none" src="http://www.dabs.com/images/product' + block['Image'] + '" /></a>'
    routername = '<div style="height:30px;"></div><a style="color:darkred; text-decoration:none; font-weight:bold;" target="_blank" title="View ' + block['Name'] + ' on Dabs.com" href="http://www.dabs.com/search?q=' + block['Name'] + '">' + block['Name'] + '</a>'
    routerprice = '<p style="float:right; margin-right:85px; font-size:36; color:maroon;">' + block['Price'] + '</p>'
    
    routerimage.lstrip()
    routername.lstrip()
    routerprice.lstrip()
    
    print '<tr><td style="text-align:center;"><div style="height:190px; background-image:url(' + "'" + 'http://www.fibrenet-project.org.uk/wp-content/uploads/2011/11/Trials-link-boxes-2.png' + "'" + ');">', routername, '</br>', routerimage, routerprice, '</div></td></tr>'

print '</table>'