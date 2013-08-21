import lxml.etree
import lxml.html
import scraperwiki
L = ['01006975']

# Load HTML
base = "http://www.lladro.com/figurines/"
for item in L:
    product = str(item)
    print product
    url = base + product
    root = lxml.html.parse(url).getroot()

# Print out fetched data
    try:
        productId = root.cssselect('td.product-detail-id')[0]
    except IndexError:
        productId = 'None'

    try:
        material = root.cssselect('p.product-detail-material')[0].text
    except IndexError:
        material = 'None'

    try:
        measure = root.cssselect('p.product-detail-measure')[0].text
        #desc = root.cssselect('p.product-detail-description2')[0]
    except IndexError:
        measure = 'None'

    print "'" + product + "';'" + material + "';'" + measure + "'"

# Write data to SQL

#    scraperwiki.sqlite.save(unique_keys=['product'], data={"product":product, "measure":measure.text, "material":material.text, "desc":0})           

#i = iter(L)
#item = i.next()


