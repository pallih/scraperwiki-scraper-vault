import mechanize 
import lxml.html
import re 
import scraperwiki 
import urllib2 
import lxml.etree 
import lxml.html 

#to go to the webpage and run a search string

kolkatahighcourt = "http://judis.nic.in/Judis_Kolkata/Dt_Of_JudQry.aspx"

br = mechanize.Browser()
response = br.open(kolkatahighcourt)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="form1")
print br.form

br["selfday"] = ["01"]
br["selfmonth"] = ["01"]
br["selfyear"] = ["2013"]
br["seltday"] = ["15"]
br["seltmonth"] = ["06"]
br["seltyear"] = ["2013"]
br["seltitletype"] = ["O"]

#what does this do with the result? I want to save it somewhere that I can act on it in the next bit

response = br.submit()
print response.read()

#to open a pdf, convert it to xml, search for a string, and -- if found -- record it and the context around it

def scrapepdf(url)
pdfdata = urllib2.urlopen(url) .read()
pdfread = scraperwiki.pdftoxml (pdfdata)

print pdfread
pdfroot = lxml.etree.fromstring (pdfread)
lines = pdfroot.findall (' .//text')
linenumber = 0
record = { }
for line in lines: 
linenumber = linenumber+1
if line.text is not None: 
mention = re.match (r' .*solar.*', line.text)
if mention: 
print line.text
print range (linenumber-2, linenumber+1)
linebefore = "EMPTY LINE" 
lineafter = "EMPTY LINE" 
incontextlist = []
if pdfroot.xpath(' .//text')[linenumber-2].text: 
linebefore = 
pdfroot.xpath(' .//text') [linenumber-2].text
incontextlist.append(linebefore)
incontextlist.append( linebefore) 
incontextlist.append( pdfroot.xpath('.// text')[ linenumber-1].text) 
if pdfroot.xpath('.// text')[ linenumber].text is not None:
lineafter = pdfroot.xpath('.// text')[ linenumber].text
incontextlist.append( lineafter) 
record[" mention in context"] = ''.join( incontextlist) 
record[" linenumber"] = linenumber 
record[" url"] = url 
print record 
scraperwiki.sqlite.save([" linenumber", "url"], record)

# to run through a page of pdfs doing this same operation

scrape_and_look_for_next_lin (result of first code section): 
html = scraperwiki.scrape(result of first code section)
root = lxml.html.fromstring(result of first code section)
pdflinks = root.cssselect("td a")
print link.attrib.get(' href')

if link is not None:
scrapepdf( next_link)import mechanize 
import lxml.html
import re 
import scraperwiki 
import urllib2 
import lxml.etree 
import lxml.html 

#to go to the webpage and run a search string

kolkatahighcourt = "http://judis.nic.in/Judis_Kolkata/Dt_Of_JudQry.aspx"

br = mechanize.Browser()
response = br.open(kolkatahighcourt)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="form1")
print br.form

br["selfday"] = ["01"]
br["selfmonth"] = ["01"]
br["selfyear"] = ["2013"]
br["seltday"] = ["15"]
br["seltmonth"] = ["06"]
br["seltyear"] = ["2013"]
br["seltitletype"] = ["O"]

#what does this do with the result? I want to save it somewhere that I can act on it in the next bit

response = br.submit()
print response.read()

#to open a pdf, convert it to xml, search for a string, and -- if found -- record it and the context around it

def scrapepdf(url)
pdfdata = urllib2.urlopen(url) .read()
pdfread = scraperwiki.pdftoxml (pdfdata)

print pdfread
pdfroot = lxml.etree.fromstring (pdfread)
lines = pdfroot.findall (' .//text')
linenumber = 0
record = { }
for line in lines: 
linenumber = linenumber+1
if line.text is not None: 
mention = re.match (r' .*solar.*', line.text)
if mention: 
print line.text
print range (linenumber-2, linenumber+1)
linebefore = "EMPTY LINE" 
lineafter = "EMPTY LINE" 
incontextlist = []
if pdfroot.xpath(' .//text')[linenumber-2].text: 
linebefore = 
pdfroot.xpath(' .//text') [linenumber-2].text
incontextlist.append(linebefore)
incontextlist.append( linebefore) 
incontextlist.append( pdfroot.xpath('.// text')[ linenumber-1].text) 
if pdfroot.xpath('.// text')[ linenumber].text is not None:
lineafter = pdfroot.xpath('.// text')[ linenumber].text
incontextlist.append( lineafter) 
record[" mention in context"] = ''.join( incontextlist) 
record[" linenumber"] = linenumber 
record[" url"] = url 
print record 
scraperwiki.sqlite.save([" linenumber", "url"], record)

# to run through a page of pdfs doing this same operation

scrape_and_look_for_next_lin (result of first code section): 
html = scraperwiki.scrape(result of first code section)
root = lxml.html.fromstring(result of first code section)
pdflinks = root.cssselect("td a")
print link.attrib.get(' href')

if link is not None:
scrapepdf( next_link)