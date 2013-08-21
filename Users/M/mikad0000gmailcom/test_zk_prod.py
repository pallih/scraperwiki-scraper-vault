import scraperwiki
import lxml.etree
import lxml.html

# Download HTML from the web
#html = scraperwiki.scrape("http://www.zhik.com/dry/ash-isotak-salopette.html")
#print html

# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
#root = lxml.html.fromstring(html) # turn our HTML into an lxml object
#h1s = root.cssselect('h1') # get all the <td> tags
#for h1 in h1s:
#    print lxml.html.tostring(h1) # the full HTML tag
#    print h1.text                # just the text inside the HTML tag


# 2. Save the data in the ScraperWiki datastore.
#for td in tds:
#     record = { "td" : td.text } # column name and value
#     scraperwiki.sqlite.save(["td"], record) # save the records one by one


# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use,
# especially with cssselect.


print help(lxml.html.parse)


#root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
root = lxml.html.parse('http://www.zhik.com/dry/ash-isotak-salopette.html')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

# Use cssselect to select elements by their css code
print root.cssselect(".product-image src")   # returns 1 element
#print root.cssselect(".LLL li")      # returns 3 elements

# extracting text from a single element
#linimble = root.cssselect("ul #nimble")[0]
#help(linimble)                       # prints the documentation for the object
#print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
#print linimble.text                  # just the text between the tag
#print linimble.tail                  # the trailing text
#print list(linimble)                 # prints the <b> object

# This recovers all the code inside the object, including any text markups like <b>
#print linimble.text + "".join(map(lxml.etree.tostring, list(linimble)))


