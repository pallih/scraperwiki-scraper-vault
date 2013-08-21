#Birmingham City University Events - Next 5 Events from Current Date
#Tutorial 1 Modifed by Andy White
#Date 14 July 2010


# import the libraries we need.  You can print out the documentation using the help() command
import scraperwiki
import urllib
help(urllib) # prints out the help documentation on this library module
import re
import datetime


# the link for single page of data
url = 'http://www2.bcu.ac.uk/events/filter'


# scrape the text from that page (ignore the decode() bit -- there's a bug that will shortly be fixed)
text = scraperwiki.scrape(url).decode('latin1')
print 'Original page source:'
print text
print 'click on the more... link above to see the whole page'

# Note how the data is you're after comes after <TABLE ...  Table4...

# This next bit extracts just that table text using regular expressions
# Please uncomment the 6 programming lines below by deleting the # character from the start of each line

eventMarkup = re.findall('(?s)<div[^>]*? id="event-[^"]*"[^>]*>(.*?)</div>', text)
print 'Table match object:', len(eventMarkup)
event = eventMarkup[0]
print
print 'Just the table text:'
print event


# This next bit separates out all the rows
# (Uncomment the next 4 lines and click run again)
rows = re.findall('(?si)<span class="date">(.*?)</span>', event)
print
#print 'The list of row contents (difficult to read because the linefeeds (\\n) have been escaped, but look for the commas):'
print rows

data = { }   # this is where we are going to put the result

# This next section loops through each row on its own
#print 'Look at each row on its own'
for event in eventMarkup:
    #print event 
    #print

    eventDetailMarkup = re.findall('(?si)<span class="date">(.*?)</span>', event)
    #print eventDetailMarkup[0]
    data["Event Date"] = eventDetailMarkup[0] 

    eventDetailMarkup = re.findall('(?si)<a[^>]*?>(.*?)</a>', event)
    #print eventDetailMarkup[0]
    data["Event Name"] = eventDetailMarkup[0] 

    eventDetailMarkup = re.findall('(?si)<p class="intro">(.*?)<a', event)
    #print eventDetailMarkup[0]
    data["Event Detail"] = eventDetailMarkup[0] 
    scraperwiki.datastore.save(unique_keys=['Event Date', 'Event Name'], data=data, latlng=data.pop('latlng', None), silent=True)
    
print "The data is now represented in the dict ('lookup table') data:"
print data



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


