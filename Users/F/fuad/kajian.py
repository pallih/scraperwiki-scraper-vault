# (extracts the values to use.  more sections are needed below to help show what functions to call next)

import mechanize 
from BeautifulSoup import BeautifulSoup

url = "http://kajian.net/kajian-audio"
br = mechanize.Browser()
br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print "--------------------"
    print form
    print "br.forms()[%d] br.select_form(name='%s')" % (i, form.name)
    br.form = allforms[i]  #  br.select_form(name=form.name) works only if name is not None
    
    # loop through the controls in the form
    for control in br.form.controls:
        if not control.name:
            print " - type=", (control.type)
            continue

        # (could group the controls by type)
        r = [ ]
        r.append(" - type=%s, name=%s, value=%s, disabled=%s, readonly=%s" % \
                 (control.type, control.name, br[control.name], control.disabled, control.readonly))
        if control.type == 'radio':
            for item in control.items:
                r.append("    name=%s" % (item.name))

        if control.type == 'select':
            for item in control.items:
                r.append("     value=%s, labels=%s" % (str(item), [label.text  for label in item.get_labels()]))
        print "\n".join(r)

r = [ "Links:" ]
for link in br.links():
    r.append("   %s" % str(link))
print "\n".join(r)

