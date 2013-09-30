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
ravi=['34',
      '5',
      '7',
      '45',
      '6',
      '7'
      '8',
]
print ravi
print
def b(x,y):
    import re
    def a1(str):
     return float(re.findall(r'\d+',str)[0])
    return cmp(a1(x),a1(y))
ravi.sort(b)
print ravi 


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
ravi=['34',
      '5',
      '7',
      '45',
      '6',
      '7'
      '8',
]
print ravi
print
def b(x,y):
    import re
    def a1(str):
     return float(re.findall(r'\d+',str)[0])
    return cmp(a1(x),a1(y))
ravi.sort(b)
print ravi 


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