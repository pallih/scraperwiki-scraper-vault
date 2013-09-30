import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup

# Blank Python

for x in range(20):
    page_number = x + 1
    
    page = urllib2.urlopen("http://www.usnews.com/education/best-high-schools/national-rankings/spp%2B100/page+"+str(page_number))

    soup = BeautifulSoup(page)

    school_table = soup.findAll('table')[0]
    
    schools = school_table.findAll('tr')
    print schools

    #itercars = iter(cars)
    #next(itercars)
    #for car in itercars:
        # do work

    iterschools = iter(schools)
    next(iterschools)

    counter = 0
    for school in schools:
        school_rank = school.findAll(attrs={"class":"rankings-score"})
        
        print school_rank
        if counter== 1:
              break
        counter = 1
        



    #school_names = soup.findAll(attrs={"class":"school-name"})
    #for school_name in school_namess:
        #school = school_name.find("a").string
        #print school

    #for school_name in school_names:
        #school = school_name.find("a").string
        #print school

    #school_name_div = soup.findAll(attrs={"class":"school-name"})[0].find('a').string #school
    #school_name = school_name_div.findAll("a").string
    #print school_name_div

    #school_rank = soup.findAll(attrs={"class":"rankings-score"}) #rank
    #print school_rank

    #school_address = soup.findAll(attrs={"class":"school-csz"}) #address
    #print school_address

    #school_district = soup.findAll(attrs={"class":"school-district"}) #district
    #print school_district



        


    
    
import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup

# Blank Python

for x in range(20):
    page_number = x + 1
    
    page = urllib2.urlopen("http://www.usnews.com/education/best-high-schools/national-rankings/spp%2B100/page+"+str(page_number))

    soup = BeautifulSoup(page)

    school_table = soup.findAll('table')[0]
    
    schools = school_table.findAll('tr')
    print schools

    #itercars = iter(cars)
    #next(itercars)
    #for car in itercars:
        # do work

    iterschools = iter(schools)
    next(iterschools)

    counter = 0
    for school in schools:
        school_rank = school.findAll(attrs={"class":"rankings-score"})
        
        print school_rank
        if counter== 1:
              break
        counter = 1
        



    #school_names = soup.findAll(attrs={"class":"school-name"})
    #for school_name in school_namess:
        #school = school_name.find("a").string
        #print school

    #for school_name in school_names:
        #school = school_name.find("a").string
        #print school

    #school_name_div = soup.findAll(attrs={"class":"school-name"})[0].find('a').string #school
    #school_name = school_name_div.findAll("a").string
    #print school_name_div

    #school_rank = soup.findAll(attrs={"class":"rankings-score"}) #rank
    #print school_rank

    #school_address = soup.findAll(attrs={"class":"school-csz"}) #address
    #print school_address

    #school_district = soup.findAll(attrs={"class":"school-district"}) #district
    #print school_district



        


    
    
