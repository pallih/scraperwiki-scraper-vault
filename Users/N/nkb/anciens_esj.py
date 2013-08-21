import scraperwiki
import re
import math
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

# This function applies the regex to the page
def regexHTML(html, expression):
    
    regex = re.compile(expression)
       
    match = regex.findall(html)
        
    name = ""
    
    if match:
        name = match[0]
    
    return name

base_url = "http://esj-lille.fr/annuaire/pages/afficher_contact.php?id=";

#finds how many records are in the DB already
scraperwiki.sqlite.attach('anciens_esj') 
num_rows = scraperwiki.sqlite.execute('SELECT COALESCE(MAX(id)+1, 0) FROM `anciens_esj`.swdata')

#extracts the number of records in the DB
start = num_rows['data'][0][0]
end = start + 5000

#Gets down to the actual scraping
for x in range(start, end):

    url = base_url + str(x)

    try:

        html = scraperwiki.scrape(url)
        
        # Looks for the data
        name = regexHTML(html, "<strong>Renseignements personnels :<\/strong><br \/>(.*?)<br \/>")
        job_title = regexHTML(html, "<span>Fonctions : <\/span>(.*?)<br \/>")
        company = regexHTML(html, "<strong>Entreprise :<\/strong> <b>(.*?)<\/b>")
        filiere = regexHTML(html, "<span>Filière : <\/span>(.*?)<br \/>")
        promotion = regexHTML(html, "<span>Promotion : <\/span>(.*?)<br \/>")
        home_country = regexHTML(html, "<span>Pays d'origine : <\/span>(.*?)<br \/>")
        
        #stores the data into an object
        data = {
              'id' : x,
              'name' : name,
              'job_title' : job_title,
              'company' : company,
              'filiere' : filiere,
              'promotion' : promotion,
              'home_country' : home_country
            }
        
        print data
        
        #saves the object
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

    except:
        pass

