"""Converting jsonduit.com's demo to Python for comparison."""

import lxml.html

from scraperwiki.datastore import save


# First a few boilerplate functions to mimic the jsonduit/jQuery API.
# You can cut-and-paste this into your own scrapers.

def getElementById(id, node):
    return node.cssselect("[id=%s]" % id)[0]

def getElements(attributes, node):
    css = ""
    for name, value in attributes.items():
        css += "[%s=%s]" % (name, value)
    return node.cssselect(css)

def getElementsByTagName(tag, node):
    return node.cssselect(tag)


# Now download and extract the page (cut-and-pastable if you fix the URL).

url = "http://stackoverflow.com/questions/tagged/ajax+json"
page = lxml.html.parse(url).getroot()


# And then we get on to the scraping part.
# Compare it to the "Example Feed" "Transform Code" at http://JSonduit.com/


questionContainer = getElementById("questions", page)

for item in getElements({"class": "question-summary"}, questionContainer):
    question = getElementsByTagName("h3", item)[0]
    save(['url', 'title'], {
        "url": "http://stackoverflow.com" + question[0].attrib['href'],
        "title": question[0].text })
"""Converting jsonduit.com's demo to Python for comparison."""

import lxml.html

from scraperwiki.datastore import save


# First a few boilerplate functions to mimic the jsonduit/jQuery API.
# You can cut-and-paste this into your own scrapers.

def getElementById(id, node):
    return node.cssselect("[id=%s]" % id)[0]

def getElements(attributes, node):
    css = ""
    for name, value in attributes.items():
        css += "[%s=%s]" % (name, value)
    return node.cssselect(css)

def getElementsByTagName(tag, node):
    return node.cssselect(tag)


# Now download and extract the page (cut-and-pastable if you fix the URL).

url = "http://stackoverflow.com/questions/tagged/ajax+json"
page = lxml.html.parse(url).getroot()


# And then we get on to the scraping part.
# Compare it to the "Example Feed" "Transform Code" at http://JSonduit.com/


questionContainer = getElementById("questions", page)

for item in getElements({"class": "question-summary"}, questionContainer):
    question = getElementsByTagName("h3", item)[0]
    save(['url', 'title'], {
        "url": "http://stackoverflow.com" + question[0].attrib['href'],
        "title": question[0].text })
