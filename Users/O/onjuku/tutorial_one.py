# Tutorial One
## note that I made a few changes to this tutorial to make it clearer
## for folks coming after me.
## DEBUG .............. If you uncommment the next line, it could help you debug possible issues that appear
## PYTHON_TIP ......... I'm teaching you a trick about python
## YOU_SHOULD_KNOW .... You'll be able to use this later
## NOTE ............... general comments


## NOTE: required before any other code (comments not included)
import scraperwiki  


## YOU_SHOULD_KNOW: this is where you put your target url 
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")

## DEBUG: make sure I found the page
# print html


## YOU_SHOULD_KNOW: the lxml.html library is from python and is the preferred (at least here)
## method for parsing html/css pages using python.
import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    ## NOTE: I use the following so that I know the script is running
    ## This slows down the script run, though.
    print data
    

    ## PYTHON_TIP: saving the data should come in the loop.  Since python loops
    ## are delimited by indentation (instead of 'begin/end' or '{ }'), the save
    ## command 'scraperwiki.sqlite.save' is at this level.
 #   scraperwiki.sqlite.save(unique_keys=['country'], data=data)


## PYTHON_TIP: try doing the following:
## (1) comment out the save command above
## (2) uncomment the save command below
## You should end up saving only the last produced data since the save command
## below is not in the for loop.
scraperwiki.sqlite.save(unique_keys=['country'], data=data)


## NOTE: tell the user where to see the data
print "see data tab"




