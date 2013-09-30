import scraperwiki

# Blank Python

###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://api.plone.org/Plone/2.5.3/private/PasswordResetTool/private/mechanize._mechanize.Browser-class.html
###############################################################################
import mechanize 
from BeautifulSoup import BeautifulSoup

# We're scraping the National Lottery grants form. You can
# replace this with the URL you're interested in. 
br = mechanize.Browser()
url = "http://www.primuslabs.com/mangos/allaudits.aspx"
br.open(url)
first = br.open(url)

br.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=o.9,*/*;q=0.8'),('Accept-Encoding','gzip, deflate'),('Accept-Language','en-us,en;q=0.5'),('Connection','keep-alive'),('Cookie','__utma=21362340.370330388.  1333586008.1333586008.1333586008.1;  __utmz=21362340.1333586008.1.  1.utmcsr=(direct)|utmccn=(  direct)|utmcmd=(none); ASP.NET_SessionId=  qd3ocl2yjqskzh551li0mjzk'),('Host','www.primuslabs.com'),('Referer','http://www.primuslabs.com/mangos/allaudits.aspx'),('User-Agent','Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko/20100101 Firefox/11.0')]

#--------------------------------------------------------------------------------------
# Loop through all the forms on the page, and print some information about each one.
# This should work with your own URL.
#--------------------------------------------------------------------------------------
for form in br.forms():
    print "--------------------"
    print "Form name : " + form.name 
    br.select_form(name=form.name)
    
    # loop through the controls in the form
    print "Controls:"
    for control in br.form.controls:
        if not control.name:
            print " - (type) =", (control.type)
            continue
            
        print " - (name, type, value) =", (control.name, control.type, br[control.name])

        # loop through all the options in any select (drop-down) controls
        if control.type == 'select':
            for item in control.items:
                print " - - - (value, labels) =", (str(item), [label.text  for label in item.get_labels()])


#--------------------------------------------------------------------------------------
# Next, let's submit the main form.
#--------------------------------------------------------------------------------------

# First, tell Mechanize which form to submit.
# If your form didn't have a CSS name attribute, use 'nr' instead 
# - e.g. br.select_form(nr=0) to find the first form on the page. 
br.select_form(name='form1')

# Set the fields:


br["Allaudits2:cboGroupBy"] = ["0"] #(Not Grouped)
br["Allaudits2:cboAuditor"] = ["0"] #All Auditor types
br["Allaudits2:cboAudit"] = ["0"] #All Audit Types
br["Allaudits2:cboEntities"] = ["0"] #All Entity Types
br["Allaudits2:cboProduct"] = ["0"] #All Products

# and submit the form
br.submit()

# We can now start processing it as normal
soup = BeautifulSoup(br.response().read())
print soup
print br.response().read()
import scraperwiki

# Blank Python

###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://api.plone.org/Plone/2.5.3/private/PasswordResetTool/private/mechanize._mechanize.Browser-class.html
###############################################################################
import mechanize 
from BeautifulSoup import BeautifulSoup

# We're scraping the National Lottery grants form. You can
# replace this with the URL you're interested in. 
br = mechanize.Browser()
url = "http://www.primuslabs.com/mangos/allaudits.aspx"
br.open(url)
first = br.open(url)

br.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=o.9,*/*;q=0.8'),('Accept-Encoding','gzip, deflate'),('Accept-Language','en-us,en;q=0.5'),('Connection','keep-alive'),('Cookie','__utma=21362340.370330388.  1333586008.1333586008.1333586008.1;  __utmz=21362340.1333586008.1.  1.utmcsr=(direct)|utmccn=(  direct)|utmcmd=(none); ASP.NET_SessionId=  qd3ocl2yjqskzh551li0mjzk'),('Host','www.primuslabs.com'),('Referer','http://www.primuslabs.com/mangos/allaudits.aspx'),('User-Agent','Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko/20100101 Firefox/11.0')]

#--------------------------------------------------------------------------------------
# Loop through all the forms on the page, and print some information about each one.
# This should work with your own URL.
#--------------------------------------------------------------------------------------
for form in br.forms():
    print "--------------------"
    print "Form name : " + form.name 
    br.select_form(name=form.name)
    
    # loop through the controls in the form
    print "Controls:"
    for control in br.form.controls:
        if not control.name:
            print " - (type) =", (control.type)
            continue
            
        print " - (name, type, value) =", (control.name, control.type, br[control.name])

        # loop through all the options in any select (drop-down) controls
        if control.type == 'select':
            for item in control.items:
                print " - - - (value, labels) =", (str(item), [label.text  for label in item.get_labels()])


#--------------------------------------------------------------------------------------
# Next, let's submit the main form.
#--------------------------------------------------------------------------------------

# First, tell Mechanize which form to submit.
# If your form didn't have a CSS name attribute, use 'nr' instead 
# - e.g. br.select_form(nr=0) to find the first form on the page. 
br.select_form(name='form1')

# Set the fields:


br["Allaudits2:cboGroupBy"] = ["0"] #(Not Grouped)
br["Allaudits2:cboAuditor"] = ["0"] #All Auditor types
br["Allaudits2:cboAudit"] = ["0"] #All Audit Types
br["Allaudits2:cboEntities"] = ["0"] #All Entity Types
br["Allaudits2:cboProduct"] = ["0"] #All Products

# and submit the form
br.submit()

# We can now start processing it as normal
soup = BeautifulSoup(br.response().read())
print soup
print br.response().read()
