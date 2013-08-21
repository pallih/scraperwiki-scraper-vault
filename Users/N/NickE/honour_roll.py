import scraperwiki
import lxml.html
import mechanize
import re

for i in range(539970, 800000):
    url = ("http://www.awm.gov.au/research/people/roll_of_honour/person.asp?p="+str(i))
    print url
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    response = br.open(url)

    html = response.read()
    
    try:
        root = lxml.html.fromstring(html)
        name = root.cssselect(".pagetitle")[0]
        name = name.text.split("- ")
        name = name[1]
        
        c=[]
        record = root.cssselect("#rohperson")
        for p in record:
            c.append (lxml.etree.tostring(p))

        record = c[0]

        try:
            recordSplit = record.split("<strong>Service number:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            serviceNo = recordSplit[0]
        
        except:
            serviceNo = "na"
    
        try:
            recordSplit = record.split("<strong>Rank:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            rank = recordSplit[0]
        
        except:
            rank = "na"
        
        try:
            recordSplit = record.split("<strong>Unit:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            unit = recordSplit[0]
        
        except:
            unit = "na"
        
    
        try:
            recordSplit = record.split("<strong>Service:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            service = recordSplit[0]
        
        except:
            service = "na"
        
        try:
            recordSplit = record.split("<strong>Conflict:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            conflict = recordSplit[0]
        
        except:
            conflict = "na"
        
        try:
            recordSplit = record.split("<strong>Date of death:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            dateOfDeath = recordSplit[0]
        
        except:
            dateOfDeath = "na"
    
        try:
            recordSplit = record.split("<strong>Place of death:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            placeOfDeath = recordSplit[0]
        
        except:
            placeOfDeath = "na"
    
        try:
            recordSplit = record.split("<strong>Cause of death:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            causeOfDeath = recordSplit[0]
        
        except:
            causeOfDeath = "na"
    
        try:
            recordSplit = record.split("<strong>Cemetery or memorial details:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            cemetery = recordSplit[0]
        
        except:
            cemetery = "na"
    
        try:
            recordSplit = record.split("<strong>Source:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            source = recordSplit[0]
        
        except:
            source = "na"
    
    
        print ("Name: " + name) 
        print ("Service Number:" + serviceNo)
        print ("Rank:" + rank)
        print ("Unit:" + unit) 
        print ("Service:" + service)
        print ("Conflict:" + conflict) 
        print ("Date of Death:" + dateOfDeath)
        print ("Place of Death:" + placeOfDeath)
        print ("Cause of Death:" + causeOfDeath)
        print ("Cemetery or memorial details:" + cemetery)  
        print ("Source" + source)
        
        data = {}
        data['name'] = name
        data['service_no'] = serviceNo
        data['rank'] = rank
        data['unit'] = unit
        data['service'] = service
        data['conflict'] = conflict
        data['date_of_death'] = dateOfDeath
        data['place_of_death'] = placeOfDeath
        data['cause_of_death'] = causeOfDeath
        data['cemetery_or_memorial'] = cemetery
        data['source'] = source
        scraperwiki.sqlite.save(unique_keys=["name"], data=data)
            

    except:
        print "no url"    

    


    
    

    

     import scraperwiki
import lxml.html
import mechanize
import re

for i in range(539970, 800000):
    url = ("http://www.awm.gov.au/research/people/roll_of_honour/person.asp?p="+str(i))
    print url
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    response = br.open(url)

    html = response.read()
    
    try:
        root = lxml.html.fromstring(html)
        name = root.cssselect(".pagetitle")[0]
        name = name.text.split("- ")
        name = name[1]
        
        c=[]
        record = root.cssselect("#rohperson")
        for p in record:
            c.append (lxml.etree.tostring(p))

        record = c[0]

        try:
            recordSplit = record.split("<strong>Service number:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            serviceNo = recordSplit[0]
        
        except:
            serviceNo = "na"
    
        try:
            recordSplit = record.split("<strong>Rank:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            rank = recordSplit[0]
        
        except:
            rank = "na"
        
        try:
            recordSplit = record.split("<strong>Unit:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            unit = recordSplit[0]
        
        except:
            unit = "na"
        
    
        try:
            recordSplit = record.split("<strong>Service:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            service = recordSplit[0]
        
        except:
            service = "na"
        
        try:
            recordSplit = record.split("<strong>Conflict:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            conflict = recordSplit[0]
        
        except:
            conflict = "na"
        
        try:
            recordSplit = record.split("<strong>Date of death:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            dateOfDeath = recordSplit[0]
        
        except:
            dateOfDeath = "na"
    
        try:
            recordSplit = record.split("<strong>Place of death:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            placeOfDeath = recordSplit[0]
        
        except:
            placeOfDeath = "na"
    
        try:
            recordSplit = record.split("<strong>Cause of death:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            causeOfDeath = recordSplit[0]
        
        except:
            causeOfDeath = "na"
    
        try:
            recordSplit = record.split("<strong>Cemetery or memorial details:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            cemetery = recordSplit[0]
        
        except:
            cemetery = "na"
    
        try:
            recordSplit = record.split("<strong>Source:</strong>")
            recordSplit = recordSplit[1].split("</p>")
            source = recordSplit[0]
        
        except:
            source = "na"
    
    
        print ("Name: " + name) 
        print ("Service Number:" + serviceNo)
        print ("Rank:" + rank)
        print ("Unit:" + unit) 
        print ("Service:" + service)
        print ("Conflict:" + conflict) 
        print ("Date of Death:" + dateOfDeath)
        print ("Place of Death:" + placeOfDeath)
        print ("Cause of Death:" + causeOfDeath)
        print ("Cemetery or memorial details:" + cemetery)  
        print ("Source" + source)
        
        data = {}
        data['name'] = name
        data['service_no'] = serviceNo
        data['rank'] = rank
        data['unit'] = unit
        data['service'] = service
        data['conflict'] = conflict
        data['date_of_death'] = dateOfDeath
        data['place_of_death'] = placeOfDeath
        data['cause_of_death'] = causeOfDeath
        data['cemetery_or_memorial'] = cemetery
        data['source'] = source
        scraperwiki.sqlite.save(unique_keys=["name"], data=data)
            

    except:
        print "no url"    

    


    
    

    

     