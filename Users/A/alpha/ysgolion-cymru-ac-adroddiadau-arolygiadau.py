url = "http://www.estyn.gov.uk/cymraeg/gwybodaeth-am-arolygiadau/adroddiadau-arolygu/"
# (extracts the values to use.  more sections are needed below to help show what functions to call next)

import mechanize
from BeautifulSoup import BeautifulSoup
#import lxml.etreex
import re

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
#        if control.type == 'radio':
#           for item in control.items:
#                r.append("    name=%s" % (item.name))
#
        if control.type == 'select':
            for item in control.items:
                r.append("     value=%s, labels=%s" % (str(item), [label.text  for label in item.get_labels()]))
        print "\n".join(r)

print br.title()
br.select_form(name='provider_search_1')
br.form['searchType'] = ['43'] #43=Ysgolion cynradd
#     value=56, labels=['Ysgolion uwchradd']
#     value=57, labels=['Ysgolion arbennig']
#     value=25, labels=['Meithrinfeydd a gynhelir']

br.response
base_url ='http://www.estyn.gov.uk/cymraeg/gwybodaeth-am-arolygiadau/adroddiadau-arolygu/'
print br.submit()
soup = BeautifulSoup(br.response().read())
tud_nesa = soup.find('a',{"class": "next"})
next_link = tud_nesa['href']
next_url = base_url + next_link
#atags = soup.findAll('a')
#print atags
#for atag_inst in atags:
#    atag = atag_inst.find(text=re.compile("Next"))
#    if atag:  
#        next_link = atag_inst['href']
print next_link
#            if next_link:
#                next_url = base_url + next_link['href']
print next_url
#                scrape_and_look_for_next_link(next_url)



#soup = BeautifulSoup(br.response().read())
#h1_tags = soup.findAll('h1')
#print h1_tags
#r = [ "Links:" ]
#for link in br.links():
#    r.append("   %s" % str(link))
#print "\n".join(r)
url = "http://www.estyn.gov.uk/cymraeg/gwybodaeth-am-arolygiadau/adroddiadau-arolygu/"
# (extracts the values to use.  more sections are needed below to help show what functions to call next)

import mechanize
from BeautifulSoup import BeautifulSoup
#import lxml.etreex
import re

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
#        if control.type == 'radio':
#           for item in control.items:
#                r.append("    name=%s" % (item.name))
#
        if control.type == 'select':
            for item in control.items:
                r.append("     value=%s, labels=%s" % (str(item), [label.text  for label in item.get_labels()]))
        print "\n".join(r)

print br.title()
br.select_form(name='provider_search_1')
br.form['searchType'] = ['43'] #43=Ysgolion cynradd
#     value=56, labels=['Ysgolion uwchradd']
#     value=57, labels=['Ysgolion arbennig']
#     value=25, labels=['Meithrinfeydd a gynhelir']

br.response
base_url ='http://www.estyn.gov.uk/cymraeg/gwybodaeth-am-arolygiadau/adroddiadau-arolygu/'
print br.submit()
soup = BeautifulSoup(br.response().read())
tud_nesa = soup.find('a',{"class": "next"})
next_link = tud_nesa['href']
next_url = base_url + next_link
#atags = soup.findAll('a')
#print atags
#for atag_inst in atags:
#    atag = atag_inst.find(text=re.compile("Next"))
#    if atag:  
#        next_link = atag_inst['href']
print next_link
#            if next_link:
#                next_url = base_url + next_link['href']
print next_url
#                scrape_and_look_for_next_link(next_url)



#soup = BeautifulSoup(br.response().read())
#h1_tags = soup.findAll('h1')
#print h1_tags
#r = [ "Links:" ]
#for link in br.links():
#    r.append("   %s" % str(link))
#print "\n".join(r)
