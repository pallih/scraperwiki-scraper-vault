# View of Tutorial One
## note that I made a few changes to this tutorial to make it clearer
## for folks coming after me.
## DEBUG .............. If you uncommment the next line, it could help you debug possible issues that appear
## PYTHON_TIP ......... I'm teaching you a trick about python
## YOU_SHOULD_KNOW .... You'll be able to use this later
## NOTE ............... general comments

## NOTE: required before any other code (comments not included)
import scraperwiki           


## PYTHON_TIP: use variables for values that show up multiple times or when you
## want to copy/paste scripts and just change the values in one place.
db_store = 'tutorial_one'
scraperwiki.sqlite.attach(db_store)


## DEBUG: make sure I can print!
# print "This is a <em>fragment</em> of HTML."


## YOU_SHOULD_KNOW: the data you are selecting in your view comes directly from
## the url of your scraper.  Since this scraper is based on the url:
##    http://scraperwiki.com/scrapers/tutorial_one/
## we use 'tutorial_one' (set above in the variable 'db_store') to reference
## this data.  The 'swdata' appears to be a construct of scraperwiki so that's
## why we are reading 'from tutorial_one.swdata' below.
data = scraperwiki.sqlite.select(
    """* from %s.swdata 
    order by years_in_school desc limit 10""" % db_store
)


## DEBUG: see that I actually collected data
# print data


## NOTE: Below is the pretty view of the data
print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"


# View of Tutorial One
## note that I made a few changes to this tutorial to make it clearer
## for folks coming after me.
## DEBUG .............. If you uncommment the next line, it could help you debug possible issues that appear
## PYTHON_TIP ......... I'm teaching you a trick about python
## YOU_SHOULD_KNOW .... You'll be able to use this later
## NOTE ............... general comments

## NOTE: required before any other code (comments not included)
import scraperwiki           


## PYTHON_TIP: use variables for values that show up multiple times or when you
## want to copy/paste scripts and just change the values in one place.
db_store = 'tutorial_one'
scraperwiki.sqlite.attach(db_store)


## DEBUG: make sure I can print!
# print "This is a <em>fragment</em> of HTML."


## YOU_SHOULD_KNOW: the data you are selecting in your view comes directly from
## the url of your scraper.  Since this scraper is based on the url:
##    http://scraperwiki.com/scrapers/tutorial_one/
## we use 'tutorial_one' (set above in the variable 'db_store') to reference
## this data.  The 'swdata' appears to be a construct of scraperwiki so that's
## why we are reading 'from tutorial_one.swdata' below.
data = scraperwiki.sqlite.select(
    """* from %s.swdata 
    order by years_in_school desc limit 10""" % db_store
)


## DEBUG: see that I actually collected data
# print data


## NOTE: Below is the pretty view of the data
print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"


