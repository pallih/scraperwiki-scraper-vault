import scraperwiki
import csv


# https://groups.google.com/forum/#!msg/scraperwiki/4kXc4qAz1Ak/HN0UNXY0GkQJ
'''
Scraperwiki will not have access to your local files, unless you run a 
webserver on your computer. 

This isn´t actually that hard to do with programs like PageKite 
(http://pagekite.net/) that allow you to have a (temporary if you 
like) webserver on your computer that servers files, without worrying 
about domain names, routers, ports or DNS. 

Even easier would be to put your csv files in a public dropbox 
(www.dropbox.com) folder. Files in the public dropbox folder have a 
url that you can use to access it. Here is a tutorial on that: 
https://www.dropbox.com/help/16 

http://db.tt/Iecm7zWp
https://www.dropbox.com/sh/fenwmibwj42b8cw/4x3vDkhec9

'''

print "Test CSV writing ..."

RESULTS = [ ['apple','cherry','orange','pineapple','strawberry'] ]

#print RESULTS

resultFile = open("myoutput.csv",'wb')
#resultFile = open("c:\output.csv",'wb')
wr = csv.writer(resultFile, dialect='excel')
wr.writerows(RESULTS)


print "End."
 