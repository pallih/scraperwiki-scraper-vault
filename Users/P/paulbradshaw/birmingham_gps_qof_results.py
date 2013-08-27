###############################################################################
# Documentation is here: 
# http://api.plone.org/Plone/2.5.3/private/PasswordResetTool/private/mechanize._mechanize.Browser-class.html
###############################################################################
import mechanize 
from BeautifulSoup import BeautifulSoup

# This is the URL for the search box for the NHS Quality & Outcomes Framework (QOF) database.  
url = "http://www.qof.ic.nhs.uk/search.asp"
br = mechanize.Browser()
br.open(url)

#--------------------------------------------------------------------------------------
# Loop through all the forms on the page, and print some information about each one.
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
br.select_form(name='search_form')

# Set the fields: here we're looking for results from a freetext search for Birmingham

br["freetext"] = "Birmingham"
# The page has some JavaScript to set other fields after submitting the form
# We can tell from the onClick="search_for_results()" attached to the submit button
# Looking at that function in the JavaScript file tells us which extra fields to set

# These fields are read-only, so change that
br.form.set_all_readonly(False)

br["do_search"] = "1"
br["current_action"] = "search"

# and submit the form
br.submit()

# We can now start processing it as normal
soup = BeautifulSoup(br.response().read())
print soup
h1_tags = soup.findAll('h1')
print h1_tags###############################################################################
# Documentation is here: 
# http://api.plone.org/Plone/2.5.3/private/PasswordResetTool/private/mechanize._mechanize.Browser-class.html
###############################################################################
import mechanize 
from BeautifulSoup import BeautifulSoup

# This is the URL for the search box for the NHS Quality & Outcomes Framework (QOF) database.  
url = "http://www.qof.ic.nhs.uk/search.asp"
br = mechanize.Browser()
br.open(url)

#--------------------------------------------------------------------------------------
# Loop through all the forms on the page, and print some information about each one.
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
br.select_form(name='search_form')

# Set the fields: here we're looking for results from a freetext search for Birmingham

br["freetext"] = "Birmingham"
# The page has some JavaScript to set other fields after submitting the form
# We can tell from the onClick="search_for_results()" attached to the submit button
# Looking at that function in the JavaScript file tells us which extra fields to set

# These fields are read-only, so change that
br.form.set_all_readonly(False)

br["do_search"] = "1"
br["current_action"] = "search"

# and submit the form
br.submit()

# We can now start processing it as normal
soup = BeautifulSoup(br.response().read())
print soup
h1_tags = soup.findAll('h1')
print h1_tags###############################################################################
# Documentation is here: 
# http://api.plone.org/Plone/2.5.3/private/PasswordResetTool/private/mechanize._mechanize.Browser-class.html
###############################################################################
import mechanize 
from BeautifulSoup import BeautifulSoup

# This is the URL for the search box for the NHS Quality & Outcomes Framework (QOF) database.  
url = "http://www.qof.ic.nhs.uk/search.asp"
br = mechanize.Browser()
br.open(url)

#--------------------------------------------------------------------------------------
# Loop through all the forms on the page, and print some information about each one.
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
br.select_form(name='search_form')

# Set the fields: here we're looking for results from a freetext search for Birmingham

br["freetext"] = "Birmingham"
# The page has some JavaScript to set other fields after submitting the form
# We can tell from the onClick="search_for_results()" attached to the submit button
# Looking at that function in the JavaScript file tells us which extra fields to set

# These fields are read-only, so change that
br.form.set_all_readonly(False)

br["do_search"] = "1"
br["current_action"] = "search"

# and submit the form
br.submit()

# We can now start processing it as normal
soup = BeautifulSoup(br.response().read())
print soup
h1_tags = soup.findAll('h1')
print h1_tags###############################################################################
# Documentation is here: 
# http://api.plone.org/Plone/2.5.3/private/PasswordResetTool/private/mechanize._mechanize.Browser-class.html
###############################################################################
import mechanize 
from BeautifulSoup import BeautifulSoup

# This is the URL for the search box for the NHS Quality & Outcomes Framework (QOF) database.  
url = "http://www.qof.ic.nhs.uk/search.asp"
br = mechanize.Browser()
br.open(url)

#--------------------------------------------------------------------------------------
# Loop through all the forms on the page, and print some information about each one.
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
br.select_form(name='search_form')

# Set the fields: here we're looking for results from a freetext search for Birmingham

br["freetext"] = "Birmingham"
# The page has some JavaScript to set other fields after submitting the form
# We can tell from the onClick="search_for_results()" attached to the submit button
# Looking at that function in the JavaScript file tells us which extra fields to set

# These fields are read-only, so change that
br.form.set_all_readonly(False)

br["do_search"] = "1"
br["current_action"] = "search"

# and submit the form
br.submit()

# We can now start processing it as normal
soup = BeautifulSoup(br.response().read())
print soup
h1_tags = soup.findAll('h1')
print h1_tags