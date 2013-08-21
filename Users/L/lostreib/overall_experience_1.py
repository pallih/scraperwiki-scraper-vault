import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup

# Blank Python

page = urllib2.urlopen("http://www.usnews.com/education/best-high-schools/national-rankings/spp+100")
    
soup = BeautifulSoup(page)

#table_one = soup.findAll(attrs={"class":"ranking-data"})
#print table_one

school_name = soup.findAll(attrs={"class":"school-name"}) #school
print school_name

school_rank = soup.findAll(attrs={"class":"rankings-score"}) #rank
print school_rank

school_address = soup.findAll(attrs={"class":"school-csz"}) #rank
print school_address

school_district = soup.findAll(attrs={"class":"school-district"}) #rank
print school_district



        


    
    
