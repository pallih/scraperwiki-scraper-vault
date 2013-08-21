import scraperwiki

# Blank Python

import mechanize

br = mechanize.Browser()
br.open("http://everything2.org/")
for i in br.forms(): # show what forms are available in the website
    print i 
br.select_form('loginform')
br['user']='scraperwiki'
br['passwd']='password'

response = br.submit() # get the html of the page once you're logged in.
html= response.read() 


