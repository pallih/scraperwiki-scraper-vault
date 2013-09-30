import scraperwiki
import lxml.etree
import lxml.html
import time 

def scrapeTable(root, numId):
    
    #annonces
    for annonce in root.cssselect("div#primaryResults"):

        #enregistrement des resultats
        record = {}      
        
        for uneAnnonce in annonce.cssselect("table tr.odd"):

            #company name
            for nomCompany in uneAnnonce.cssselect("div.companyContainer a"):
                record["company"]=nomCompany.text
                
            #annonceName
            for annonceName in uneAnnonce.cssselect("div.jobTitleContainer a"):
                record["annonceName"]=annonceName.text
        
            #salaire
            for salaire in uneAnnonce.cssselect("div.companyContainer div.fnt13"):
                record["salaire"]=salaire.text
        
            #date
            for parution in uneAnnonce.cssselect("td.fnt4 div.fnt20"):
                if "Aujourd" in parution.text.split("'")[0]:
                    record["parution "]=time.strftime('%d/%m/%y', time.localtime())
                else:
                    record["parution "]=parution.text
    
            #region
            for region in uneAnnonce.cssselect("div.jobLocationSingleLine a"):
                record["region"]=region.text
    
            #id
            record["id"]=numId

            #save in datastore
            scraperwiki.sqlite.save(["id"], record)
            numId=numId+1

        for uneAnnonce in annonce.cssselect("table tr.even"):

            #company name
            for nomCompany in uneAnnonce.cssselect("div.companyContainer a"):
                record["company"]=nomCompany.text
                
            #annonceName
            for annonceName in uneAnnonce.cssselect("div.jobTitleContainer a"):
                record["annonceName"]=annonceName.text
        
            #salaire
            for salaire in uneAnnonce.cssselect("div.companyContainer div.fnt13"):
                record["salaire"]=salaire.text
        
            #date
            for parution in uneAnnonce.cssselect("td.fnt4 div.fnt20"):
                if "Aujourd" in parution.text.split("'")[0]:
                    print time.strftime('%d/%m/%y', time.localtime())
                    record["parution "]=time.strftime('%d/%m/%y', time.localtime())
                else:
                    record["parution "]=parution.text
    
            #region
            for region in uneAnnonce.cssselect("div.jobLocationSingleLine a"):
                record["region"]=region.text
    
            #id
            record["id"]=numId
            
            #print record["region"]
    
            #save in datastore
            scraperwiki.sqlite.save(["id"], record)
            numId=numId+1



#start
sUrlBase="http://jobsearch.monster.com/search/?where=03063"
numId=0

for page in range(20):
    page=page+2
    sUrl=sUrlBase + str(page) + "&cy=fr"
    print sUrl

    html = scraperwiki.scrape(sUrl)
    root = lxml.html.fromstring(html)

    scrapeTable(root, numId)
    numId=numId+20 
import scraperwiki
import lxml.etree
import lxml.html
import time 

def scrapeTable(root, numId):
    
    #annonces
    for annonce in root.cssselect("div#primaryResults"):

        #enregistrement des resultats
        record = {}      
        
        for uneAnnonce in annonce.cssselect("table tr.odd"):

            #company name
            for nomCompany in uneAnnonce.cssselect("div.companyContainer a"):
                record["company"]=nomCompany.text
                
            #annonceName
            for annonceName in uneAnnonce.cssselect("div.jobTitleContainer a"):
                record["annonceName"]=annonceName.text
        
            #salaire
            for salaire in uneAnnonce.cssselect("div.companyContainer div.fnt13"):
                record["salaire"]=salaire.text
        
            #date
            for parution in uneAnnonce.cssselect("td.fnt4 div.fnt20"):
                if "Aujourd" in parution.text.split("'")[0]:
                    record["parution "]=time.strftime('%d/%m/%y', time.localtime())
                else:
                    record["parution "]=parution.text
    
            #region
            for region in uneAnnonce.cssselect("div.jobLocationSingleLine a"):
                record["region"]=region.text
    
            #id
            record["id"]=numId

            #save in datastore
            scraperwiki.sqlite.save(["id"], record)
            numId=numId+1

        for uneAnnonce in annonce.cssselect("table tr.even"):

            #company name
            for nomCompany in uneAnnonce.cssselect("div.companyContainer a"):
                record["company"]=nomCompany.text
                
            #annonceName
            for annonceName in uneAnnonce.cssselect("div.jobTitleContainer a"):
                record["annonceName"]=annonceName.text
        
            #salaire
            for salaire in uneAnnonce.cssselect("div.companyContainer div.fnt13"):
                record["salaire"]=salaire.text
        
            #date
            for parution in uneAnnonce.cssselect("td.fnt4 div.fnt20"):
                if "Aujourd" in parution.text.split("'")[0]:
                    print time.strftime('%d/%m/%y', time.localtime())
                    record["parution "]=time.strftime('%d/%m/%y', time.localtime())
                else:
                    record["parution "]=parution.text
    
            #region
            for region in uneAnnonce.cssselect("div.jobLocationSingleLine a"):
                record["region"]=region.text
    
            #id
            record["id"]=numId
            
            #print record["region"]
    
            #save in datastore
            scraperwiki.sqlite.save(["id"], record)
            numId=numId+1



#start
sUrlBase="http://jobsearch.monster.com/search/?where=03063"
numId=0

for page in range(20):
    page=page+2
    sUrl=sUrlBase + str(page) + "&cy=fr"
    print sUrl

    html = scraperwiki.scrape(sUrl)
    root = lxml.html.fromstring(html)

    scrapeTable(root, numId)
    numId=numId+20 
