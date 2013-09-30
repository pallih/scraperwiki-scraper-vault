import scraperwiki
sourcescraper = 'wega_di_number'
scraperwiki.sqlite.attach(sourcescraper)
#############################################################################
#      // This is a View based on the Scraper: Wega di number Korsou \\     #
#                       in plain python                                     #
#                                                                           #
#                    Feel free to modify, copy                              #
#     if you modify or copy please include your twitter or FB below         #
#             Twitter : @royendgel, Facebook Royendgel Silberie             #
#                                                                           #
#                                                                           #
#############################################################################


#some variable declaration to be list

winningnumbers = []
notwinningnumbers = []



# this is to connect to the database 
data = scraperwiki.sqlite.execute("select * from swdata") 

# this declares the list of numbers 
data = data["data"][0]



for data in data:
    winningnumbers = data

#now let's generate the numbers 0000 trough 9999 and analise the data in it
for x in ["%04d" % x for x in range(9999)]:
    if x not in winningnumbers:

        notwinningnumbers.append(x)
        

print "<h1 style='color:red;'>Simple Analises</h1><br /><br /><br /><br />"

print "<h4>Some simple analisis : </h4>"
print "There are " + str() + " drawn to date <br /><br />"
print "The number most drawn is : " + str() + " Played <strong>" + str() + "</strong> Times" + " <br />"
print "winning numbers : <br />"

for series in range(10):
    #print "This is Series " + str(series) + "<br />"
    for notwinningnumbers in notwinningnumbers:
        print notwinningnumbers[0]
        if notwinningnumbers[0] == str(series):
            print "<strong>" + notwinningnumbers + "</strong><br />"


import scraperwiki
sourcescraper = 'wega_di_number'
scraperwiki.sqlite.attach(sourcescraper)
#############################################################################
#      // This is a View based on the Scraper: Wega di number Korsou \\     #
#                       in plain python                                     #
#                                                                           #
#                    Feel free to modify, copy                              #
#     if you modify or copy please include your twitter or FB below         #
#             Twitter : @royendgel, Facebook Royendgel Silberie             #
#                                                                           #
#                                                                           #
#############################################################################


#some variable declaration to be list

winningnumbers = []
notwinningnumbers = []



# this is to connect to the database 
data = scraperwiki.sqlite.execute("select * from swdata") 

# this declares the list of numbers 
data = data["data"][0]



for data in data:
    winningnumbers = data

#now let's generate the numbers 0000 trough 9999 and analise the data in it
for x in ["%04d" % x for x in range(9999)]:
    if x not in winningnumbers:

        notwinningnumbers.append(x)
        

print "<h1 style='color:red;'>Simple Analises</h1><br /><br /><br /><br />"

print "<h4>Some simple analisis : </h4>"
print "There are " + str() + " drawn to date <br /><br />"
print "The number most drawn is : " + str() + " Played <strong>" + str() + "</strong> Times" + " <br />"
print "winning numbers : <br />"

for series in range(10):
    #print "This is Series " + str(series) + "<br />"
    for notwinningnumbers in notwinningnumbers:
        print notwinningnumbers[0]
        if notwinningnumbers[0] == str(series):
            print "<strong>" + notwinningnumbers + "</strong><br />"


