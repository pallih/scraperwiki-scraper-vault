import lxml.html

url = "http://hoopdata.com/boxscores.aspx"
root = lxml.html.parse(url).getroot()

# alternatively you can use:
#   html = urllib2.urlopen(url).read()
#   root = lxml.html.fromstring(html)

print "The root element is:", root
print "The elements in this root element are:", list(root)
print "The elements two levels down are:", [ list(el)  for el in root ]

divs = root.cssselect("div")
print "There are %d elements with tag div in this page" % len(divs)
print "Their corresponding attributes are:", [div.attrib  for div in divs ]

bsdiv = root.cssselect("table.MyGridView")[0]
print "The copyright message is: ", lxml.html.tostring(bsdiv)


# Click on "Quick help" and select lxml cheat sheet for more advice
for table in root.cssselect('table.MyGridView'):
    data = {'box_score': table.text} # save data in dictionary
    # Choose unique keyname
    scraperwiki.datastore.save(unique_keys=['box_score'], data=data) 
