import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup

# Blank Python

for x in range (50):
    page_number = x + 1
    
    page = urllib2.urlopen("http://www.usnews.com/education/best-high-schools/national-rankings/spp%2B100/page+"+str(page_number))

    soup = BeautifulSoup(page)

    #school_table = soup.findAll('table')[0]
    
    #schools = school_table.findAll('tr')
    #print schools

    #school_names = soup.findAll(attrs={"class":"school-name"})
    #for school_name in school_names:
        #school = school_name.find("a").string
        #print school

    #school_districts = soup.findAll(attrs={"class":"school-district"})
    #for school_district in school_districts:
        #school = school_district.find("a").string
        #print school

    school_address = soup.findAll(attrs={"class":"school-csz"})
    print school_address

    

    #school_ranks = soup.findAll(attrs={"class":"rankings-score"})
    #print school_ranks

   