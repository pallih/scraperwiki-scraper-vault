# import a module (library) that helps us do scraping
import scraperwiki
# import another that helps us extract things from the scraped data
import lxml.html
# use that module's scrape function to grab the contents of a URL and put it in the variable HTML
html = scraperwiki.scrape("http://www.nhs.uk/Services/Trusts/GPs/DefaultView.aspx?id=5PG")
# use the lxml.html's fromstring function to grab some structured data, put in a variable called gplist
gplist = lxml.html.fromstring(html) 
# get the first <p class="child-org-name"> <a> tags from within that, put in variable called gpname
gpname = gplist.cssselect(".child-org-name a")

print list(gpname) #prints a list of elements in gpname

#print lxml.html.tostring(gpname) #only works if you add [0] or other index to end of line 10
#print map(lxml.etree.tostring, list(gpname)) #displays all results as strings
for gp in list(gpname):
     record = { "gp" : gp.text } # column name and value
     scraperwiki.sqlite.save(["gp"], record) # save the records one by one
# QUESTION: How do you grab & store the link in the <a> tag around the text?
#gpclasses = gplist.find_class("child-org-name")
#for gpclass in list(gpclasses):
#    print gpclass# import a module (library) that helps us do scraping
import scraperwiki
# import another that helps us extract things from the scraped data
import lxml.html
# use that module's scrape function to grab the contents of a URL and put it in the variable HTML
html = scraperwiki.scrape("http://www.nhs.uk/Services/Trusts/GPs/DefaultView.aspx?id=5PG")
# use the lxml.html's fromstring function to grab some structured data, put in a variable called gplist
gplist = lxml.html.fromstring(html) 
# get the first <p class="child-org-name"> <a> tags from within that, put in variable called gpname
gpname = gplist.cssselect(".child-org-name a")

print list(gpname) #prints a list of elements in gpname

#print lxml.html.tostring(gpname) #only works if you add [0] or other index to end of line 10
#print map(lxml.etree.tostring, list(gpname)) #displays all results as strings
for gp in list(gpname):
     record = { "gp" : gp.text } # column name and value
     scraperwiki.sqlite.save(["gp"], record) # save the records one by one
# QUESTION: How do you grab & store the link in the <a> tag around the text?
#gpclasses = gplist.find_class("child-org-name")
#for gpclass in list(gpclasses):
#    print gpclass# import a module (library) that helps us do scraping
import scraperwiki
# import another that helps us extract things from the scraped data
import lxml.html
# use that module's scrape function to grab the contents of a URL and put it in the variable HTML
html = scraperwiki.scrape("http://www.nhs.uk/Services/Trusts/GPs/DefaultView.aspx?id=5PG")
# use the lxml.html's fromstring function to grab some structured data, put in a variable called gplist
gplist = lxml.html.fromstring(html) 
# get the first <p class="child-org-name"> <a> tags from within that, put in variable called gpname
gpname = gplist.cssselect(".child-org-name a")

print list(gpname) #prints a list of elements in gpname

#print lxml.html.tostring(gpname) #only works if you add [0] or other index to end of line 10
#print map(lxml.etree.tostring, list(gpname)) #displays all results as strings
for gp in list(gpname):
     record = { "gp" : gp.text } # column name and value
     scraperwiki.sqlite.save(["gp"], record) # save the records one by one
# QUESTION: How do you grab & store the link in the <a> tag around the text?
#gpclasses = gplist.find_class("child-org-name")
#for gpclass in list(gpclasses):
#    print gpclass# import a module (library) that helps us do scraping
import scraperwiki
# import another that helps us extract things from the scraped data
import lxml.html
# use that module's scrape function to grab the contents of a URL and put it in the variable HTML
html = scraperwiki.scrape("http://www.nhs.uk/Services/Trusts/GPs/DefaultView.aspx?id=5PG")
# use the lxml.html's fromstring function to grab some structured data, put in a variable called gplist
gplist = lxml.html.fromstring(html) 
# get the first <p class="child-org-name"> <a> tags from within that, put in variable called gpname
gpname = gplist.cssselect(".child-org-name a")

print list(gpname) #prints a list of elements in gpname

#print lxml.html.tostring(gpname) #only works if you add [0] or other index to end of line 10
#print map(lxml.etree.tostring, list(gpname)) #displays all results as strings
for gp in list(gpname):
     record = { "gp" : gp.text } # column name and value
     scraperwiki.sqlite.save(["gp"], record) # save the records one by one
# QUESTION: How do you grab & store the link in the <a> tag around the text?
#gpclasses = gplist.find_class("child-org-name")
#for gpclass in list(gpclasses):
#    print gpclass# import a module (library) that helps us do scraping
import scraperwiki
# import another that helps us extract things from the scraped data
import lxml.html
# use that module's scrape function to grab the contents of a URL and put it in the variable HTML
html = scraperwiki.scrape("http://www.nhs.uk/Services/Trusts/GPs/DefaultView.aspx?id=5PG")
# use the lxml.html's fromstring function to grab some structured data, put in a variable called gplist
gplist = lxml.html.fromstring(html) 
# get the first <p class="child-org-name"> <a> tags from within that, put in variable called gpname
gpname = gplist.cssselect(".child-org-name a")

print list(gpname) #prints a list of elements in gpname

#print lxml.html.tostring(gpname) #only works if you add [0] or other index to end of line 10
#print map(lxml.etree.tostring, list(gpname)) #displays all results as strings
for gp in list(gpname):
     record = { "gp" : gp.text } # column name and value
     scraperwiki.sqlite.save(["gp"], record) # save the records one by one
# QUESTION: How do you grab & store the link in the <a> tag around the text?
#gpclasses = gplist.find_class("child-org-name")
#for gpclass in list(gpclasses):
#    print gpclass