# mechanize is a very powerful library that can be used to explore and fill in web-forms.
# Here are some inline-able code to help you along

import mechanize 
import re
import scraperwiki

url = "http://www.wipo.int/pctdb/en/index.jsp"
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(url)
br.select_form("frm")
response = br.submit()
text = response.read()
plinks = re.findall("(?s)<!--#ISEARCH-FETCH-LINK--><A HREF='(http://www.wipo.int/.*?)'.*?>([^<]*)</A>.*?<TD[^>]*>\s*(\d\d\.\d\d\.\d\d\d\d)?", text)
for plink in plinks:
    print plink
    
    scraperwiki.datastore.save(unique_keys=["url"], data={"url":plink[0], "title":plink[1], "datea":plink[2]})
    
    
# future work: 
# fill in the application date entry in the form (note all patents are done on one day a week)
# pagenate through the 1000+ entries on that date
# scrape each destination page and extract applicant, country, category, etc.



# mechanize is a very powerful library that can be used to explore and fill in web-forms.
# Here are some inline-able code to help you along

import mechanize 
import re
import scraperwiki

url = "http://www.wipo.int/pctdb/en/index.jsp"
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(url)
br.select_form("frm")
response = br.submit()
text = response.read()
plinks = re.findall("(?s)<!--#ISEARCH-FETCH-LINK--><A HREF='(http://www.wipo.int/.*?)'.*?>([^<]*)</A>.*?<TD[^>]*>\s*(\d\d\.\d\d\.\d\d\d\d)?", text)
for plink in plinks:
    print plink
    
    scraperwiki.datastore.save(unique_keys=["url"], data={"url":plink[0], "title":plink[1], "datea":plink[2]})
    
    
# future work: 
# fill in the application date entry in the form (note all patents are done on one day a week)
# pagenate through the 1000+ entries on that date
# scrape each destination page and extract applicant, country, category, etc.



# mechanize is a very powerful library that can be used to explore and fill in web-forms.
# Here are some inline-able code to help you along

import mechanize 
import re
import scraperwiki

url = "http://www.wipo.int/pctdb/en/index.jsp"
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(url)
br.select_form("frm")
response = br.submit()
text = response.read()
plinks = re.findall("(?s)<!--#ISEARCH-FETCH-LINK--><A HREF='(http://www.wipo.int/.*?)'.*?>([^<]*)</A>.*?<TD[^>]*>\s*(\d\d\.\d\d\.\d\d\d\d)?", text)
for plink in plinks:
    print plink
    
    scraperwiki.datastore.save(unique_keys=["url"], data={"url":plink[0], "title":plink[1], "datea":plink[2]})
    
    
# future work: 
# fill in the application date entry in the form (note all patents are done on one day a week)
# pagenate through the 1000+ entries on that date
# scrape each destination page and extract applicant, country, category, etc.



# mechanize is a very powerful library that can be used to explore and fill in web-forms.
# Here are some inline-able code to help you along

import mechanize 
import re
import scraperwiki

url = "http://www.wipo.int/pctdb/en/index.jsp"
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(url)
br.select_form("frm")
response = br.submit()
text = response.read()
plinks = re.findall("(?s)<!--#ISEARCH-FETCH-LINK--><A HREF='(http://www.wipo.int/.*?)'.*?>([^<]*)</A>.*?<TD[^>]*>\s*(\d\d\.\d\d\.\d\d\d\d)?", text)
for plink in plinks:
    print plink
    
    scraperwiki.datastore.save(unique_keys=["url"], data={"url":plink[0], "title":plink[1], "datea":plink[2]})
    
    
# future work: 
# fill in the application date entry in the form (note all patents are done on one day a week)
# pagenate through the 1000+ entries on that date
# scrape each destination page and extract applicant, country, category, etc.



# mechanize is a very powerful library that can be used to explore and fill in web-forms.
# Here are some inline-able code to help you along

import mechanize 
import re
import scraperwiki

url = "http://www.wipo.int/pctdb/en/index.jsp"
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(url)
br.select_form("frm")
response = br.submit()
text = response.read()
plinks = re.findall("(?s)<!--#ISEARCH-FETCH-LINK--><A HREF='(http://www.wipo.int/.*?)'.*?>([^<]*)</A>.*?<TD[^>]*>\s*(\d\d\.\d\d\.\d\d\d\d)?", text)
for plink in plinks:
    print plink
    
    scraperwiki.datastore.save(unique_keys=["url"], data={"url":plink[0], "title":plink[1], "datea":plink[2]})
    
    
# future work: 
# fill in the application date entry in the form (note all patents are done on one day a week)
# pagenate through the 1000+ entries on that date
# scrape each destination page and extract applicant, country, category, etc.



# mechanize is a very powerful library that can be used to explore and fill in web-forms.
# Here are some inline-able code to help you along

import mechanize 
import re
import scraperwiki

url = "http://www.wipo.int/pctdb/en/index.jsp"
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(url)
br.select_form("frm")
response = br.submit()
text = response.read()
plinks = re.findall("(?s)<!--#ISEARCH-FETCH-LINK--><A HREF='(http://www.wipo.int/.*?)'.*?>([^<]*)</A>.*?<TD[^>]*>\s*(\d\d\.\d\d\.\d\d\d\d)?", text)
for plink in plinks:
    print plink
    
    scraperwiki.datastore.save(unique_keys=["url"], data={"url":plink[0], "title":plink[1], "datea":plink[2]})
    
    
# future work: 
# fill in the application date entry in the form (note all patents are done on one day a week)
# pagenate through the 1000+ entries on that date
# scrape each destination page and extract applicant, country, category, etc.



# mechanize is a very powerful library that can be used to explore and fill in web-forms.
# Here are some inline-able code to help you along

import mechanize 
import re
import scraperwiki

url = "http://www.wipo.int/pctdb/en/index.jsp"
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(url)
br.select_form("frm")
response = br.submit()
text = response.read()
plinks = re.findall("(?s)<!--#ISEARCH-FETCH-LINK--><A HREF='(http://www.wipo.int/.*?)'.*?>([^<]*)</A>.*?<TD[^>]*>\s*(\d\d\.\d\d\.\d\d\d\d)?", text)
for plink in plinks:
    print plink
    
    scraperwiki.datastore.save(unique_keys=["url"], data={"url":plink[0], "title":plink[1], "datea":plink[2]})
    
    
# future work: 
# fill in the application date entry in the form (note all patents are done on one day a week)
# pagenate through the 1000+ entries on that date
# scrape each destination page and extract applicant, country, category, etc.



# mechanize is a very powerful library that can be used to explore and fill in web-forms.
# Here are some inline-able code to help you along

import mechanize 
import re
import scraperwiki

url = "http://www.wipo.int/pctdb/en/index.jsp"
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(url)
br.select_form("frm")
response = br.submit()
text = response.read()
plinks = re.findall("(?s)<!--#ISEARCH-FETCH-LINK--><A HREF='(http://www.wipo.int/.*?)'.*?>([^<]*)</A>.*?<TD[^>]*>\s*(\d\d\.\d\d\.\d\d\d\d)?", text)
for plink in plinks:
    print plink
    
    scraperwiki.datastore.save(unique_keys=["url"], data={"url":plink[0], "title":plink[1], "datea":plink[2]})
    
    
# future work: 
# fill in the application date entry in the form (note all patents are done on one day a week)
# pagenate through the 1000+ entries on that date
# scrape each destination page and extract applicant, country, category, etc.



