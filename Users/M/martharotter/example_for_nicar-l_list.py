import scraperwiki

# Blank Python

import urllib2
import re
from BeautifulSoup import BeautifulSoup

#create a file called "ward_pop.csv" 

#f = open('ward_pop.tsv', 'w')

#make the script cycle through Toronto Ward numbers 1-44 and define each number as a ward

for x in range(2,44):

    #(NOTE: I skipped 1 in the cycle because the code structure on
    #Ward 1's webpage is an outlier relative to the others. Please don't use that page as a reference)

    #load and parse the ward profile webpages one at a time 

    wardstamp = "Ward " + str(x)
    print "Getting data for " + wardstamp
    url = 'http://www.toronto.ca/wards2000/ward' + str(x) + '.htm'

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    
    #extract the sentence with the ward's total population
    
    sentence = soup.findAll('p')[1].text
    print "Now printing extracted sentence"
    print sentence

    #split the sentence up into an "array" (list) of words

    words = sentence.split()

    #extract the ward number and population from the word array

    num = str(words[1])
    pop = str(words[5])

    #write to file:

    print "Ward " + num + "\t" + pop + "\n"

    #Done! Close file.

    #f.close()
