import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup

# Blank Python

school_list = ['suny-binghamton-university','suny-college-at-oneonta','suny-purchase-college','appalachian-state-university','campbell-university','davidson-college','duke-university','east-carolina-university','elizabeth-city-state-university','elon-university','guilford-college','montreat-college','university-of-north-carolina-at-asheville','university-of-north-carolina-at-chapel-hill','university-of-north-carolina----greensboro','north-carolina-central-university','university-of-north-carolina----wilmington','university-of-north-carolina-at-pembroke','salem-college','wake-forest-university','warren-wilson-college','winston--salem-state-university','western-carolina-university','bennett-college-for-women','fayetteville-state-university','north-carolina-state-university','gardner--webb-university','high-point-university','north-carolina-a-and-t-state-university','university-of-north-carolina-at-charlotte','shaw-university','university-of-north-dakota']

#print list[0]

for thisSchool in school_list:
    #print thisSchool

    try:
        page = urllib2.urlopen("http://collegeprowler.com/" + thisSchool + "/rankings/")

        soup = BeautifulSoup(page)

        table_one = soup.findAll("table")[0]

        experience_label = table_one.findAll("td")[13] #grade
        #print experience__label

        experience__rank = table_one.findAll("td")[1] #rank
        print experience__rank

        

        
    
    except  (IndexError):
         print "Oops! Try again..."
    
    
