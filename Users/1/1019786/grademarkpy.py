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
def marks(MA,MB,MC,MD):
    print"your marks in each module is out of 100"
    print"Your  marks is", MA
    print"Your  marks is", MB
    print"Your  marks is", MC
    print"Your  marks is", MD
    Add=  MA+MB+MC+MD
    print "your total marks is " ,Add 
    if Add>=350:
       print"Well done!!!!!!Grade A"
    elif Add>=300:
        print"Good!!!!!!Grade B"
    elif Add>=250:
        print"Keep it up!!!!!!!Grade C"
    elif Add>=200:
        print"Do hard work!!!!!Grade D"
    elif Add>=150:
        print"You have only one chance to pass Grade E"
    else:    
        print"Fail..... You need hard work if you want to paas!!!!!"
            
if __name__ == '__main__':
    MA1=input("MA: ")
    MB2=input("MB: ")
    MC3=input("MC: ")
    MD4=input("MD: ")
    marks(MA1,MB2,MC3,MD4)


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