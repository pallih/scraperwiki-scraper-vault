# Warning: Only for geniuses

import mechanize
import re

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/3.0')]
br.open(url)
br.select_form(name='Form1')
br.form['txtboxSurname'] = 'a'   # search for surnames with just 'a'
request = br.form.click('btnSearch')
print request.get_data()
f0 = br.open(request).read()
print f0


br.select_form(name='Form1')
br.form.set_all_readonly(False)
br.form['__EVENTTARGET'] = 'dgPublicRegistry$_ctl14$_ctl6'  # one of the next page links at the bottom
br.form['__EVENTARGUMENT'] = ''
br.form['btnSearch'] = '1'
# Mechanize confused by generic site search submit button - disable.
print br.form.click().get_data()
br.form.find_control('nav:top_search_submit').disabled=True
request = br.form.click()

print request.get_data()
f1 = br.open(request).read()
print f1

print "Should be next page (ie false):", f0 == f1
print re.search('AARONSON', f0), re.search('AARONSON', f1)  # proves we got the same page

# Warning: Only for geniuses

import mechanize
import re

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/3.0')]
br.open(url)
br.select_form(name='Form1')
br.form['txtboxSurname'] = 'a'   # search for surnames with just 'a'
request = br.form.click('btnSearch')
print request.get_data()
f0 = br.open(request).read()
print f0


br.select_form(name='Form1')
br.form.set_all_readonly(False)
br.form['__EVENTTARGET'] = 'dgPublicRegistry$_ctl14$_ctl6'  # one of the next page links at the bottom
br.form['__EVENTARGUMENT'] = ''
br.form['btnSearch'] = '1'
# Mechanize confused by generic site search submit button - disable.
print br.form.click().get_data()
br.form.find_control('nav:top_search_submit').disabled=True
request = br.form.click()

print request.get_data()
f1 = br.open(request).read()
print f1

print "Should be next page (ie false):", f0 == f1
print re.search('AARONSON', f0), re.search('AARONSON', f1)  # proves we got the same page

# Warning: Only for geniuses

import mechanize
import re

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/3.0')]
br.open(url)
br.select_form(name='Form1')
br.form['txtboxSurname'] = 'a'   # search for surnames with just 'a'
request = br.form.click('btnSearch')
print request.get_data()
f0 = br.open(request).read()
print f0


br.select_form(name='Form1')
br.form.set_all_readonly(False)
br.form['__EVENTTARGET'] = 'dgPublicRegistry$_ctl14$_ctl6'  # one of the next page links at the bottom
br.form['__EVENTARGUMENT'] = ''
br.form['btnSearch'] = '1'
# Mechanize confused by generic site search submit button - disable.
print br.form.click().get_data()
br.form.find_control('nav:top_search_submit').disabled=True
request = br.form.click()

print request.get_data()
f1 = br.open(request).read()
print f1

print "Should be next page (ie false):", f0 == f1
print re.search('AARONSON', f0), re.search('AARONSON', f1)  # proves we got the same page

# Warning: Only for geniuses

import mechanize
import re

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/3.0')]
br.open(url)
br.select_form(name='Form1')
br.form['txtboxSurname'] = 'a'   # search for surnames with just 'a'
request = br.form.click('btnSearch')
print request.get_data()
f0 = br.open(request).read()
print f0


br.select_form(name='Form1')
br.form.set_all_readonly(False)
br.form['__EVENTTARGET'] = 'dgPublicRegistry$_ctl14$_ctl6'  # one of the next page links at the bottom
br.form['__EVENTARGUMENT'] = ''
br.form['btnSearch'] = '1'
# Mechanize confused by generic site search submit button - disable.
print br.form.click().get_data()
br.form.find_control('nav:top_search_submit').disabled=True
request = br.form.click()

print request.get_data()
f1 = br.open(request).read()
print f1

print "Should be next page (ie false):", f0 == f1
print re.search('AARONSON', f0), re.search('AARONSON', f1)  # proves we got the same page

# Warning: Only for geniuses

import mechanize
import re

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/3.0')]
br.open(url)
br.select_form(name='Form1')
br.form['txtboxSurname'] = 'a'   # search for surnames with just 'a'
request = br.form.click('btnSearch')
print request.get_data()
f0 = br.open(request).read()
print f0


br.select_form(name='Form1')
br.form.set_all_readonly(False)
br.form['__EVENTTARGET'] = 'dgPublicRegistry$_ctl14$_ctl6'  # one of the next page links at the bottom
br.form['__EVENTARGUMENT'] = ''
br.form['btnSearch'] = '1'
# Mechanize confused by generic site search submit button - disable.
print br.form.click().get_data()
br.form.find_control('nav:top_search_submit').disabled=True
request = br.form.click()

print request.get_data()
f1 = br.open(request).read()
print f1

print "Should be next page (ie false):", f0 == f1
print re.search('AARONSON', f0), re.search('AARONSON', f1)  # proves we got the same page

# Warning: Only for geniuses

import mechanize
import re

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/3.0')]
br.open(url)
br.select_form(name='Form1')
br.form['txtboxSurname'] = 'a'   # search for surnames with just 'a'
request = br.form.click('btnSearch')
print request.get_data()
f0 = br.open(request).read()
print f0


br.select_form(name='Form1')
br.form.set_all_readonly(False)
br.form['__EVENTTARGET'] = 'dgPublicRegistry$_ctl14$_ctl6'  # one of the next page links at the bottom
br.form['__EVENTARGUMENT'] = ''
br.form['btnSearch'] = '1'
# Mechanize confused by generic site search submit button - disable.
print br.form.click().get_data()
br.form.find_control('nav:top_search_submit').disabled=True
request = br.form.click()

print request.get_data()
f1 = br.open(request).read()
print f1

print "Should be next page (ie false):", f0 == f1
print re.search('AARONSON', f0), re.search('AARONSON', f1)  # proves we got the same page

# Warning: Only for geniuses

import mechanize
import re

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/3.0')]
br.open(url)
br.select_form(name='Form1')
br.form['txtboxSurname'] = 'a'   # search for surnames with just 'a'
request = br.form.click('btnSearch')
print request.get_data()
f0 = br.open(request).read()
print f0


br.select_form(name='Form1')
br.form.set_all_readonly(False)
br.form['__EVENTTARGET'] = 'dgPublicRegistry$_ctl14$_ctl6'  # one of the next page links at the bottom
br.form['__EVENTARGUMENT'] = ''
br.form['btnSearch'] = '1'
# Mechanize confused by generic site search submit button - disable.
print br.form.click().get_data()
br.form.find_control('nav:top_search_submit').disabled=True
request = br.form.click()

print request.get_data()
f1 = br.open(request).read()
print f1

print "Should be next page (ie false):", f0 == f1
print re.search('AARONSON', f0), re.search('AARONSON', f1)  # proves we got the same page

# Warning: Only for geniuses

import mechanize
import re

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/3.0')]
br.open(url)
br.select_form(name='Form1')
br.form['txtboxSurname'] = 'a'   # search for surnames with just 'a'
request = br.form.click('btnSearch')
print request.get_data()
f0 = br.open(request).read()
print f0


br.select_form(name='Form1')
br.form.set_all_readonly(False)
br.form['__EVENTTARGET'] = 'dgPublicRegistry$_ctl14$_ctl6'  # one of the next page links at the bottom
br.form['__EVENTARGUMENT'] = ''
br.form['btnSearch'] = '1'
# Mechanize confused by generic site search submit button - disable.
print br.form.click().get_data()
br.form.find_control('nav:top_search_submit').disabled=True
request = br.form.click()

print request.get_data()
f1 = br.open(request).read()
print f1

print "Should be next page (ie false):", f0 == f1
print re.search('AARONSON', f0), re.search('AARONSON', f1)  # proves we got the same page

