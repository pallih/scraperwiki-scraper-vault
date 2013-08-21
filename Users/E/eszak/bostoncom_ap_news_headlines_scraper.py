# Hi Elana,
# I'm gonna give you a few hints :-)
# ~ Zarino

import scraperwiki
import lxml.html # the html module is simpler than etree
import requests

# We request the webpage from the Boston Globe's server:
content = requests.get('http://www.boston.com/news/education/')
# The server responds with something. We print out the text (html) it gave us:
print content.text

# Feed the text/html into lxml, because it's awesome:
document = lxml.html.fromstring(content.text)

# This will print the first, second, and third headlines:
#print document.cssselect('div.padBottom10 h3 a')[0].text
#print document.cssselect('div.padBottom10 h3 a')[1].text
#print document.cssselect('div.padBottom10 h3 a')[2].text

# This will print *all* the headlines:
#for a in document.cssselect('div.padBottom10 h3 a'): 
#    print a.text
#    print a.get('href')

# Save every headline to the datastore:

# We first create a list to store our headlines,
# so we can then save the whole list in one go
# (far more efficient than saving inside a loop)
headlines = []
for a in document.cssselect('div.padBottom10 h3 a'):
    headlines.append({
        'headline': a.text,
        'url': a.get('href')
    })

# Our list is full - time to save it!
# We have to define a "key" for the database,
# that's what the "['headline']" bit does.
# If you want to learn more about database keys,
# Google it.
scraperwiki.sqlite.save(['headline'], headlines)

