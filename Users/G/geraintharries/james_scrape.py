from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import re

def webScrape():
    float counter = 4170
    float limit = 4172
    
    while counter < limit:
        houseNum = str(counter)
        webpage = urlopen("http://www.cpshomes.co.uk/lettings/properties/property_details.aspx?reference=P" + houseNum).read()
        
    regexFindURL = re.compile('Postcode: (.*)</span></li><li title="Council Tax"><span>')
    
    deface = re.findall(regexFindURL, webpage)
    
    
    
    postCode = regexFindURL