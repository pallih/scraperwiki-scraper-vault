import lxml.html

# Blank Python


doc = lxml.html.parse('http://tracking.ironmanlive.com/newathlete.php?rid=1143239954&race=florida&bib=2512&v=3.0&beta=&1360094400')

#get athlete Name
for kid in doc.xpath('/html/body/div/div[1]/h2[1]'):
    athleteName = kid.text

print(athleteName)


#basic info is in 
for kid in doc.xpath('//table[1]'):
    print lxml.etree.tostring(kid)

import lxml.html

# Blank Python


doc = lxml.html.parse('http://tracking.ironmanlive.com/newathlete.php?rid=1143239954&race=florida&bib=2512&v=3.0&beta=&1360094400')

#get athlete Name
for kid in doc.xpath('/html/body/div/div[1]/h2[1]'):
    athleteName = kid.text

print(athleteName)


#basic info is in 
for kid in doc.xpath('//table[1]'):
    print lxml.etree.tostring(kid)

