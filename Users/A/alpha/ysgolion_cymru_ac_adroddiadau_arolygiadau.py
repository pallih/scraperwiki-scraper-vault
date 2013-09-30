url="http://www.lcfclubs.com/find.asp?id=W"
# (extracts the values to use.  more sections are needed below to help show what functions to call next)

import mechanize
from BeautifulSoup import BeautifulSoup
import lxml.html
import re

br = mechanize.Browser()
response = br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print "--------------------"
    print form
    print "br.forms()[%d] br.select_form(name='%s')" % (i, form.name)
    br.form = allforms[i]  #  br.select_form(name=form.name) works only if name is not None
    
    labs = []
    # loop through the controls in the form
    for control in br.form.controls:
        if not control.name:
            print " - type=", (control.type)
            continue

        # (could group the controls by type)
        r = [ ]
        r.append(" - type=%s, name=%s, value=%s, disabled=%s, readonly=%s" % \
                 (control.type, control.name, br[control.name], control.disabled, control.readonly))
#        if control.type == 'radio':
#           for item in control.items:
#                r.append("    name=%s" % (item.name))
#
        if control.type == 'select':
            for item in control.items:
                r.append("     value=%s, labels=%s" % (str(item), [label.text  for label in item.get_labels()]))
                [labs.append(label.text)  for label in item.get_labels()]
        print "\n".join(r)

print labs  # dyma enwau'r siroedd

root = lxml.html.parse(url).getroot()

# alternatively you can use:
#   html = urllib2.urlopen(url).read()
#   root = lxml.html.fromstring(html)

print "The root element is:", root
print "The elements in this root element are:", list(root)
print "The elements two levels down are:", [ list(el)  for el in root ]

divs = root.cssselect("div")
print "There are %d elements with tag div in this page" % len(divs)
print "Their corresponding attributes are:", [div.attrib  for div in divs]

crdiv = root.cssselect("div#search")[0]
print "search 0 is ", lxml.html.tostring(crdiv)

for lab in labs:
    print lab
    br.form = list(br.forms())[1]
    br['county'] = [lab]
    try:
        response = br.submit()
        resphtml = response.read()
        #soup = BeautifulSoup(br.response().read())
        root = lxml.html.fromstring(resphtml)
        print root
        manylion= root.cssselect("div.resultline")
        print manylion
        #results = root.text_content()
        #results = root.cssselect('div','class:resultline'}
        #print results
        for el in manylion:
            print el.tag, el.attrib,el.text_content()
    except:
        print "No records"url="http://www.lcfclubs.com/find.asp?id=W"
# (extracts the values to use.  more sections are needed below to help show what functions to call next)

import mechanize
from BeautifulSoup import BeautifulSoup
import lxml.html
import re

br = mechanize.Browser()
response = br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print "--------------------"
    print form
    print "br.forms()[%d] br.select_form(name='%s')" % (i, form.name)
    br.form = allforms[i]  #  br.select_form(name=form.name) works only if name is not None
    
    labs = []
    # loop through the controls in the form
    for control in br.form.controls:
        if not control.name:
            print " - type=", (control.type)
            continue

        # (could group the controls by type)
        r = [ ]
        r.append(" - type=%s, name=%s, value=%s, disabled=%s, readonly=%s" % \
                 (control.type, control.name, br[control.name], control.disabled, control.readonly))
#        if control.type == 'radio':
#           for item in control.items:
#                r.append("    name=%s" % (item.name))
#
        if control.type == 'select':
            for item in control.items:
                r.append("     value=%s, labels=%s" % (str(item), [label.text  for label in item.get_labels()]))
                [labs.append(label.text)  for label in item.get_labels()]
        print "\n".join(r)

print labs  # dyma enwau'r siroedd

root = lxml.html.parse(url).getroot()

# alternatively you can use:
#   html = urllib2.urlopen(url).read()
#   root = lxml.html.fromstring(html)

print "The root element is:", root
print "The elements in this root element are:", list(root)
print "The elements two levels down are:", [ list(el)  for el in root ]

divs = root.cssselect("div")
print "There are %d elements with tag div in this page" % len(divs)
print "Their corresponding attributes are:", [div.attrib  for div in divs]

crdiv = root.cssselect("div#search")[0]
print "search 0 is ", lxml.html.tostring(crdiv)

for lab in labs:
    print lab
    br.form = list(br.forms())[1]
    br['county'] = [lab]
    try:
        response = br.submit()
        resphtml = response.read()
        #soup = BeautifulSoup(br.response().read())
        root = lxml.html.fromstring(resphtml)
        print root
        manylion= root.cssselect("div.resultline")
        print manylion
        #results = root.text_content()
        #results = root.cssselect('div','class:resultline'}
        #print results
        for el in manylion:
            print el.tag, el.attrib,el.text_content()
    except:
        print "No records"