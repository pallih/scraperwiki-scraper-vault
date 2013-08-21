# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 12:33:53 2011

@author: Ian Hopkinson
"""

# Functions to parse the House of Lords members interest
# Data is of the form:
# http://www.parliament.uk/mps-lords-and-offices/standards-and-interests/register-of-lords-interests/?letter=A

# Structure is:
# <h2
#   <strong>Category 1<>
#       <p
#       <p
#   <strong>Category 2<>
#       <p
#      ....

import scraperwiki
import urllib
from BeautifulSoup import BeautifulSoup
from collections import defaultdict
import csv

#As well as a flat file format I also build a dictionary but it isn't a convenient format
LordsDict=defaultdict(lambda: defaultdict(str))

LordsList=[]
CategoryList=[]
TextList=[]

#A little bit of bootstrapping here, I generated this list using an earlier version of the program
CategoriesDict={'Category 1: Directorships': '1',
 'Category 2: Remunerated employment, office, profession etc.':'2',
 'Category 3: Clients': '3',
 'Category 4: Shareholdings (a)': '4a',
 'Category 4: Shareholdings (b)': '4b',
 'Category 5: Land and property': '5',
 'Category 6: Sponsorship': '6',
 'Category 7: Overseas visits': '7',
 'Category 8: Gifts, benefits and hospitality': '8',
 'Category 9: Miscellaneous financial interests': '9',
 'Category 10: Non-financial interests (a)': '10a',
 'Category 10: Non-financial interests (b)': '10b',
 'Category 10: Non-financial interests (c)': '10c',
 'Category 10: Non-financial interests (d)': '10d',
 'Category 10: Non-financial interests (e)': '10e',
 'Nil': '11'}

LordCounter=0

# This is the root URL for the data
urlstub="http://www.parliament.uk/mps-lords-and-offices/standards-and-interests/register-of-lords-interests/?letter="

letters=map(chr, range(97, 123))

#Loop over the letters, and for each letter loop over the Lords on the page
for letter in letters:
    print "Processing letter %s" % letter
    # Get a file-like object for the Python Web site's home page.
    f = urllib.urlopen(urlstub+letter)
    # Read from the object, storing the page's contents in 's'.
    s = f.read()
    f.close()

    #Beautiful soup makes the data easy to analyse
    soup=BeautifulSoup(s)

    lords=soup.findAll("h2")

    for lord in lords:
        lordname=lord.contents[0].encode("utf-8")
        # The pages are quite nicely structed, except "Related information" looks like a lord
        if lordname=="Related information":
            break
        #print lordname
        LordCounter+=1
        s=lord
        category=""
        currenttext=""
        while 1:
            s=s.findNextSibling()
            # Have we reached next Lord?
            if getattr(s, 'name', None) == 'h2' or s is None:
                #Need to put stored string into Dictionary
                LordsList.append(lordname)
                CategoryList.append(CategoriesDict.get(category))
                TextList.append(currenttext)
                
                LordsDict[lordname][category]=currenttext
                currenttext=""            
                break
            # Have we reached a new category, if yes then store old and move on
            if getattr(s, 'name', None) == 'strong':
                #
                if len(currenttext)>0:
                    LordsList.append(lordname)
                    CategoryList.append(CategoriesDict.get(category))
                    TextList.append(currenttext)

                    LordsDict[lordname][category]=currenttext
                    currenttext=""
                category=s.contents[0].encode("utf-8")
            # Keep a list of categories
            #    if CategoriesDict.has_key(category):
            #        CategoriesDict[category]+=1
            #    else:
            #        CategoriesDict[category]=1
        # If it's p then simply add to the
            if getattr(s, 'name', None) == 'p':
                currenttext=currenttext+s.contents[0].encode("utf-8")+"|"
            #print s.contents[0].encode("utf-8")        
        #print "End of lord\n"

index=1
for i in range(0,len(LordsList)):
# This print slows things down a lot when run interactively so take it out
    #print "Raw: %s, %s, %s" % (LordsList[i],CategoryList[i],TextList[i])
    TextParts=TextList[i].split("|")
    for piece in TextParts:
        if len(piece)>1:
            #print "%d. %s, %s, %s" % (index,LordsList[i],CategoryList[i],piece)
            #Write to the datastore
            record={"ID":index,"Name":LordsList[i], "InterestCategory":CategoryList[i],"InterestDescription":piece}
            scraperwiki.sqlite.save(unique_keys=["ID"], data=record)
            index=index+1

# Output to csv
#ofile=open('LordsInterests.csv', 'wb')
#OutWriter = csv.writer(ofile, delimiter=',')

#for i in range (0,len(LordsList)): 
#    OutWriter.writerow([LordsList[i],CategoryList[i],TextList[i]])

#ofile.close()



