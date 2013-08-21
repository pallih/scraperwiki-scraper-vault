import lxml.etree
import lxml.html
import scraperwiki
L = [811248]

# Load HTML
base = "http://sales.enesco.com/business/ProductDetails.aspx?ProductID="
for item in L:
    product = str(item)
    url = base + product
    root = lxml.html.parse(url).getroot()

# Print out fetched data
    productId = root.cssselect('td.product-detail-id')[0]
    material = root.cssselect('p.product-detail-material')[0]
    measure = root.cssselect('p.product-detail-measure')[0]
    #desc = root.cssselect('p.product-detail-description2')[0]
    print "'" + product + "';'" + material.text + "';'" + measure.text + "'"

# Write data to SQL
    scraperwiki.sqlite.save(unique_keys=['product'], data={"product":product, "measure":measure.text, "material":material.text, "desc":0})           

i = iter(L)
item = i.next()


