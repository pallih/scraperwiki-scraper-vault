###############################################################################
# START HERE: Tutorial 1: Getting used to the ScraperWiki editing interface.
# Follow the actions listed with -- BLOCK CAPITALS below.
###############################################################################

# -----------------------------------------------------------------------------
# 1. Start by running a really simple Python script, just to make sure that 
# everything is working OK.
# -- CLICK THE 'RUN' BUTTON BELOW
# You should see some numbers print in the 'Console' tab below. If it doesn't work, 
# try reopening this page in a different browser - Chrome or the latest Firefox.
# -----------------------------------------------------------------------------

import turtle
print "welcome"
print "My frist programming calculator"
print "Follow the instruction please"
print "Use + for Sum"
print "Use - for Subraction"
print "Use * for Mul"
print "Use / for DIv"
num =input("enter the value please")
num2= input("enter the second value please")
a= (num+num2)
b= (num-num2)
c= (num*num2)
d= (num/num2)
option = raw_input("what would you like to do")
if option =='+':
    print "Answer is",a
if option =='-':
    print "Answer is ",b
if option =='*':
    print "Answer is ",c
if option =='/':
    print"Answer is ",d

# -----------------------------------------------------------------------------
# 2. Next, try scraping an actual web page and getting some raw HTML.
# -- UNCOMMENT THE THREE LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON AGAIN 
# You should see the raw HTML at the bottom of the 'Console' tab. 
# Click on the 'more' link to see it all, and the 'Sources' tab to see our URL - 
# you can click on the URL to see the original page. 
# -----------------------------------------------------------------------------

#import scraperwiki
#html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')
#print html

# -----------------------------------------------------------------------------
# In the next tutorial, you'll learn how to extract the useful parts
# from the raw HTML page.
# -----------------------------------------------------------------------------###############################################################################
# START HERE: Tutorial 1: Getting used to the ScraperWiki editing interface.
# Follow the actions listed with -- BLOCK CAPITALS below.
###############################################################################

# -----------------------------------------------------------------------------
# 1. Start by running a really simple Python script, just to make sure that 
# everything is working OK.
# -- CLICK THE 'RUN' BUTTON BELOW
# You should see some numbers print in the 'Console' tab below. If it doesn't work, 
# try reopening this page in a different browser - Chrome or the latest Firefox.
# -----------------------------------------------------------------------------

import turtle
print "welcome"
print "My frist programming calculator"
print "Follow the instruction please"
print "Use + for Sum"
print "Use - for Subraction"
print "Use * for Mul"
print "Use / for DIv"
num =input("enter the value please")
num2= input("enter the second value please")
a= (num+num2)
b= (num-num2)
c= (num*num2)
d= (num/num2)
option = raw_input("what would you like to do")
if option =='+':
    print "Answer is",a
if option =='-':
    print "Answer is ",b
if option =='*':
    print "Answer is ",c
if option =='/':
    print"Answer is ",d

# -----------------------------------------------------------------------------
# 2. Next, try scraping an actual web page and getting some raw HTML.
# -- UNCOMMENT THE THREE LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON AGAIN 
# You should see the raw HTML at the bottom of the 'Console' tab. 
# Click on the 'more' link to see it all, and the 'Sources' tab to see our URL - 
# you can click on the URL to see the original page. 
# -----------------------------------------------------------------------------

#import scraperwiki
#html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')
#print html

# -----------------------------------------------------------------------------
# In the next tutorial, you'll learn how to extract the useful parts
# from the raw HTML page.
# -----------------------------------------------------------------------------