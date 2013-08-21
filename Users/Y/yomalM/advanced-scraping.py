# This tutorial is to help you parse a single page from the Lottery grants database
# We get to these pages using the mechanize library, but that's a different problem.
# The lesson here is about cleaning up the data for one record

# For the full solution, look at: http://scraperwiki.com/scrapers/show/uk-lottery-grants-1/code/


# The slide show at the Journalism Summer school is
#   http://docs.google.com/present/view?id=dcfvj9d_95fnp73tc9


# import the libraries we need.  You can print out the documentation using the help() command
import scraperwiki
import urllib
help(urllib) # prints out the help documentation on this library module
import re
import datetime


# the link for single page of data
url = 'http://www.lottery.culture.gov.uk/details.asp?ID=6181000&DBID=AE'


# scrape the text from that page (ignore the decode() bit -- there's a bug that will shortly be fixed)
text = scraperwiki.scrape(url).decode('latin1')
print 'Original page source:'
print text
print 'click on the more... link above to see the whole page'

# Note how the data is you're after comes after <TABLE ...  Table4...

# This next bit extracts just that table text using regular expressions
# Please uncomment the 6 programming lines below by deleting the # character from the start of each line

#table4 = re.findall('(?s)<TABLE[^>]*? ID="Table4"[^>]*>(.*?)</TABLE>', text)
#print 'Table match object:', len(table4)
#tabletext = table4[0]
#print
#print 'Just the table text:'
#print tabletext


# This next bit separates out all the rows
# (Uncomment the next 4 lines and click run again)
#rows = re.findall("(?si)<tr[^>]*>(.*?)</tr>", tabletext)
#print 
#print 'The list of row contents (difficult to read because the linefeeds (\\n) have been escaped, but look for the commas):'
#print rows

data = { }   # this is where we are going to put the result

# This next section loops through each row on its own
#print 'Look at each row on its own'
#for row in rows:
#    print row

#    rowlookup = re.findall('<font size="-1">(.*?)</font></span></td>\s*<TD width="\*">(.*?)&nbsp;</td>', row)
#    key = rowlookup[0][0]
#    value = rowlookup[0][1]
#    print key, '=', value
#    data[key] = value    

#print "The data is now represented in the dict ('lookup table') data:"
#print data

# Now we do the clean-up stages

# First turn the monetary amount into a number
#amount = data["Award Amount"]
#print "Original form:", amount
#amount = amount[1:]  # discard the pound sign
#print u"With first character, the £ sign removed:", amount

#print int(amount)    # gives an error

#amount = re.sub(',', '', amount)
#print "With commas removed:", amount

# now we can set it back as an integer number
#data["Award Amount"] = int(amount)


# Now convert the date into a real date object
#datelookup = re.findall("(\d\d)/(\d\d)/(\d\d\d\d)", data["Award Date"])
#print "Matched date is:", datelookup
#cleandate = datetime.datetime(year=int(datelookup[0][2]), month=int(datelookup[0][1]), day=int(datelookup[0][0]))

# Set the date into the field
#data["Award Date"] = cleandate

#print "Finally, the cleaned up date is:", data

# We still should give the constituency and local authorities unique ids to before the job is really done!


