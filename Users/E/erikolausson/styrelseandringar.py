# -*- coding: utf-8 -*-


import scraperwiki

from mechanize import Browser
import mechanize
import lxml.html

user = "af1862"
password = "lejon"


datum = 20130226
datum_intervall = str(datum-1)+"-"+str(datum)
print datum_intervall
limit = 1000

radnr = 0

br = Browser()
br.set_handle_robots(False)

br.open("http://www.ad.se", timeout=300.0)

br.select_form(name="LOGIN")

br["xUSER"]=user
br["PASSWD"]=password

response = br.submit() #log in to Affärsdata


#print response.read()

#print list(br.links())
response1 = br.follow_link(text="F\xf6retag")

#print response1.read()

response2 = br.follow_link(text="Dagens")

#print br
#print response2.read()

br.select_form(name="formet")

br.form["limit"]=["1000"] #setting the limit to numer of companies in search to 1000. Optimal would be 5000 however...

#print br.form
javascript_numbers= br.form["oldss"]
#print javascript_numbers
javascript_numbers1=javascript_numbers[2:12] #jag vet inte vad de här siffrorna betyder, mer än att de hänger ihop med datumen. Hur som helst måste de till för att få rätt url när vi vill komma runt javascripten.
#print str(javascript_numbers1)
javascript_numbers2=javascript_numbers[34:44]
#print str(javascript_numbers2)

#print list(br.links())

#print br.find_link(text="s\xf6kresultat")
#response3 = br.follow_link(text="s\xf6kresultat")
#print response3.read()

#--------------för att komma runt javascripten som skapar följande url:

response4 = br.open("http://www.ad.se/ff/kung/kung_main.php?subaction=1&oldss=%28+"+str(javascript_numbers1)+"+%3C%3D+datumintervall+%3C%3D+"+str(javascript_numbers2)+"+%29&limit="+str(limit)+"&kategori=0&datum_spec="+datum_intervall+"&uss=%28+datumintervall+%3D+"+datum_intervall+"+%29&start=1&end=50&layout_change=&limit_change=1&layout=&kungid_rapport=&todo=1") #Verkar funka. (17 april 2013)

#response4 = br.open("http://www.ad.se/ff/kung/kung_main.php?subaction=1&oldss=%28+1358377200+%3C%3D+datumintervall+%3C%3D+1358463600+%29&limit=" + str(limit)+"&kategori=0&datum_spec="+datum_intervall+"&uss=%28+datumintervall+%3D+"+datum_intervall+"+%29&start=1&end=50&layout_change=&limit_change=1&layout=&kungid_rapport=&todo=1")  #OBS! Inte säkert att det här funkar även senare - vilken roll spelar texten "datumintervall" till exempel? (18 januari 2013)

#response4 = br.open("http://www.ad.se/ff/kung/kung_main.php?subaction=1&oldss=%28+"+str(1366149600)+"+%3C%3D+datumintervall+%3C%3D+1366236000+%29&limit="+str(limit)+"&kategori=0&datum_spec="+datum_intervall+"&uss=%28+datumintervall+%3D+"+datum_intervall+"+%29&start=1&end=50&layout_change=&limit_change=1&layout=&kungid_rapport=&todo=1")  #OBS! Inte säkert att det här funkar även senare - vilken roll spelar texten "datumintervall" till exempel? (18 januari 2013)

print response4.read()


br.select_form(name="ffsok")

response5 = br.submit() #Vi har nu en lista på alla företag med kunggörelser det aktuella datumintervallet. Dags att välja ut dem från Skåne.
#print response5.read()

print "rad 74"

#br.select_form(name="mainform")

#print br.form
#br.form["lan[]"]=["12"] #skåne har värde 12
#print br.form
#response6 = br.submit() #Detta ger oss en lista på företag med kungörelser i Skåne.
#print response6.read() #Hit verkar allt fungera som det ska (19 arpil 2013)

br.select_form(name="mainform")

#print "rad 97"  
#print br.form
#print "rad 99"
#br.form["lan[]"]=["0"] #26 april: testar att försöka sudda ut länet för att få koden längre ner att fungera. Men hur?
#print br.form




br.form.find_control("dummy3").readonly=False #så att vi kan manipulera värdena
br.form.find_control("dummy2").readonly=False
br.form.find_control("dummy1").readonly=False  


br.form["dummy1"]="3"
br.form["dummy2"]="filter"
br.form["dummy3"]= "akt"  #detta är för att bara få aktiva AB. De övriga två kontrollerna vet jag inte exakt vad de gör...
print br.form

print "nu är vi här"
response7 = br.submit() # 26 april: skumt, detta fungerar om jag inte tidigare preciserat vilket län jag vill söka i. Med länet utvalt får jag däremot noll träffar. Torde ha något att göra med vad br.form har för värden på sina olika attribut, men vad?

br.select_form(name="mainform")

dagens_org_nr = str(br.find_control("uss")) #här går vi "bakvägen" genom att extrahera strängen som innehåller samtliga org-nr för bolag med kunggörelser i dag.
#print br.form
dagens_org_nr=dagens_org_nr[30:-15] #en enda lång sträng med de orgnr som har kunggörelser i dag. Denna sträng stoppar vi tillbaka i formuläret lite längre ner.
print "dagens org_nr:"+dagens_org_nr
print "längd dagens org nr:" + str(len(dagens_org_nr))

print br
#print response7.read()

response8 = br.follow_link(text="F\xf6retag")
#print br

br.select_form(name="mainform")
print "mainform, rad 129"
print br.form
#br.form.find_control("limit").readonly = False #sätt till False så att vi kan ändra värdet
#br.form["limit"] = ["250"] #så att vi får alla träffar på en lång lista
#print br.form
br.form["orgnr"]=dagens_org_nr #här stoppar vi tillbaka strängen med de org_nr som har kunggörelser i dag. 
br.form["lan[]"]=["12"] #Ange samtidigt skåne som län för att bara få dem från skåne.
print "före submit"
print br.form

response9 = br.submit() #nu har vi en lista på de bolag som har kunggörelser i dag och säte i skåne. Kruxet är att de bara visas 25 i taget. (22 maj)
#print response9.read()

br.select_form(name="mainform")
print "efter submit"
print br.form
br.form.find_control("limit").readonly = False #sätt till False så att vi kan ändra värdet
br.form.find_control("end").readonly = False
br.form["limit"] = "250" #så att vi får alla träffar på en lång lista
br.form["end"]= "250"
print "ny version av formen"
print br.form

respone9b = br.submit()

br.select_form(name="mainform")
print "efter andra submit" #PROBLEM: Den checkbox-control som heter orgnrs[] och som vi vill använda för att extrahera listan på organisationsnummer i skåne försvinner när vi kör en andra submit. (24 maj)
print br.form

#print br.form.find_control("orgnrs[]").items[0]
dagens_skanska_orgnr = br.form.find_control("orgnrs[]").items[:]   #detta ger en lista på org_nr för skånska bolag som har kunggörelser det akutella datumet
print "antal org_nr: " + str(len(dagens_skanska_orgnr))
#print str(dagens_skanska_orgnr[0])+"detta är listan: "+str(dagens_skanska_orgnr[1])
#print br.form["orgnrs[]"]

for d in range(len(dagens_skanska_orgnr)):

    br.open("http://www.allabolag.se", timeout=300.0)
    print br

    br.select_form(name="f_search")
    #print br.form
    br["what"]=str(dagens_skanska_orgnr[d])
    response10=br.submit()#26 april: so far, so good. Nästa steg blir att skrapa upp den info om bolaget vi vill ha, främst verksamhet, omsättning och, via bolagsveket, vad kunggörelsen gäller.
    #print "rad 159"
    #print response10.read()
    #print list(br.links())
    root = lxml.html.fromstring(response10.read())
    namn = root.cssselect("td.reportTitle h1")[0] 
    namn = namn.text_content()
    #print type(namn)
    namn= namn.encode('utf-8') #namn har typen ElementUnicodeResult. Detta konverterar det till en sträng
    #print type(namn)
    print namn


    oms = root.cssselect("tr.bgLightPink td")
    print oms[14].text_content()

    br.back()

    br.select_form(name="f_search")
    br["what"]=namn
    response11 = br.submit()

    #print response11.read()

    root = lxml.html.fromstring(response11.read())
    print root.cssselect("td.text11grey6 span") #här verkar det bli fel ibland, dvs. listan som returneras är tom. Varför? 22 maj 2013
    if len(root.cssselect("td.text11grey6 span"))>1:

        verksamhet = root.cssselect("td.text11grey6 span")[1]
        verksamhet =  verksamhet.tail
    else:
        verksamhet = "Verksamhet ej funnen"    
    
    print verksamhet
    #for c in range(7):
    #    print oms[c].text_content()

    #response11= br.follow_link(text="Verksamhet & Status")  

    #verksamhet = root.cssselect("div.reportFrame a.linkOne")
    #for c in range(len(verksamhet)):
    #    print verksamhet[c].text_content()

    br.open("https://sokarende.bolagsverket.se/mia/", timeout=300.0) #undersök vad kunggörelsen handlar om hos Bolagsveket
    br.select_form(name="arende-sok-form")
    print br.form

    br["arende-sok-form:sokterm"]=str(dagens_skanska_orgnr[d])
    response12=br.submit()
    #print response12.read(

    root = lxml.html.fromstring(response12.read())
    arende_lista = root.cssselect("dl.orginfo li")

    #print "length " + str(len(arende_lista)) 

    for c in range(len(arende_lista)):
        print arende_lista[c].text

    arenden =[0,0,0,0,0]
    for c in range(5):
        if c<len(arende_lista):
            arenden[c]=arende_lista[c].text
        else:
            arenden[c]="-"
    #arenden[0:2]=arende_lista
    print arenden[0]
    print arenden[4]
    #arenden[0:len(arende_lista)]=arenden_lista

    scraperwiki.sqlite.save(unique_keys=["row"], data={"row":d, "name":namn, "oms":oms[14].text_content(), "verksamhet": verksamhet, "regarding":arenden[0], "regardingtwo":arenden[1], "regardingthree":arenden[2]}) 

    #for c in range(len(arende_lista)):
    #    if c>4:
    #        break
    #    else:
    #        scraperwiki.sqlite.save(unique_keys=["row"], data={"row":radnr, "name":namn, "pris":pris[h].text})    
    # print arende_lista[c].text


# -*- coding: utf-8 -*-


import scraperwiki

from mechanize import Browser
import mechanize
import lxml.html

user = "af1862"
password = "lejon"


datum = 20130226
datum_intervall = str(datum-1)+"-"+str(datum)
print datum_intervall
limit = 1000

radnr = 0

br = Browser()
br.set_handle_robots(False)

br.open("http://www.ad.se", timeout=300.0)

br.select_form(name="LOGIN")

br["xUSER"]=user
br["PASSWD"]=password

response = br.submit() #log in to Affärsdata


#print response.read()

#print list(br.links())
response1 = br.follow_link(text="F\xf6retag")

#print response1.read()

response2 = br.follow_link(text="Dagens")

#print br
#print response2.read()

br.select_form(name="formet")

br.form["limit"]=["1000"] #setting the limit to numer of companies in search to 1000. Optimal would be 5000 however...

#print br.form
javascript_numbers= br.form["oldss"]
#print javascript_numbers
javascript_numbers1=javascript_numbers[2:12] #jag vet inte vad de här siffrorna betyder, mer än att de hänger ihop med datumen. Hur som helst måste de till för att få rätt url när vi vill komma runt javascripten.
#print str(javascript_numbers1)
javascript_numbers2=javascript_numbers[34:44]
#print str(javascript_numbers2)

#print list(br.links())

#print br.find_link(text="s\xf6kresultat")
#response3 = br.follow_link(text="s\xf6kresultat")
#print response3.read()

#--------------för att komma runt javascripten som skapar följande url:

response4 = br.open("http://www.ad.se/ff/kung/kung_main.php?subaction=1&oldss=%28+"+str(javascript_numbers1)+"+%3C%3D+datumintervall+%3C%3D+"+str(javascript_numbers2)+"+%29&limit="+str(limit)+"&kategori=0&datum_spec="+datum_intervall+"&uss=%28+datumintervall+%3D+"+datum_intervall+"+%29&start=1&end=50&layout_change=&limit_change=1&layout=&kungid_rapport=&todo=1") #Verkar funka. (17 april 2013)

#response4 = br.open("http://www.ad.se/ff/kung/kung_main.php?subaction=1&oldss=%28+1358377200+%3C%3D+datumintervall+%3C%3D+1358463600+%29&limit=" + str(limit)+"&kategori=0&datum_spec="+datum_intervall+"&uss=%28+datumintervall+%3D+"+datum_intervall+"+%29&start=1&end=50&layout_change=&limit_change=1&layout=&kungid_rapport=&todo=1")  #OBS! Inte säkert att det här funkar även senare - vilken roll spelar texten "datumintervall" till exempel? (18 januari 2013)

#response4 = br.open("http://www.ad.se/ff/kung/kung_main.php?subaction=1&oldss=%28+"+str(1366149600)+"+%3C%3D+datumintervall+%3C%3D+1366236000+%29&limit="+str(limit)+"&kategori=0&datum_spec="+datum_intervall+"&uss=%28+datumintervall+%3D+"+datum_intervall+"+%29&start=1&end=50&layout_change=&limit_change=1&layout=&kungid_rapport=&todo=1")  #OBS! Inte säkert att det här funkar även senare - vilken roll spelar texten "datumintervall" till exempel? (18 januari 2013)

print response4.read()


br.select_form(name="ffsok")

response5 = br.submit() #Vi har nu en lista på alla företag med kunggörelser det aktuella datumintervallet. Dags att välja ut dem från Skåne.
#print response5.read()

print "rad 74"

#br.select_form(name="mainform")

#print br.form
#br.form["lan[]"]=["12"] #skåne har värde 12
#print br.form
#response6 = br.submit() #Detta ger oss en lista på företag med kungörelser i Skåne.
#print response6.read() #Hit verkar allt fungera som det ska (19 arpil 2013)

br.select_form(name="mainform")

#print "rad 97"  
#print br.form
#print "rad 99"
#br.form["lan[]"]=["0"] #26 april: testar att försöka sudda ut länet för att få koden längre ner att fungera. Men hur?
#print br.form




br.form.find_control("dummy3").readonly=False #så att vi kan manipulera värdena
br.form.find_control("dummy2").readonly=False
br.form.find_control("dummy1").readonly=False  


br.form["dummy1"]="3"
br.form["dummy2"]="filter"
br.form["dummy3"]= "akt"  #detta är för att bara få aktiva AB. De övriga två kontrollerna vet jag inte exakt vad de gör...
print br.form

print "nu är vi här"
response7 = br.submit() # 26 april: skumt, detta fungerar om jag inte tidigare preciserat vilket län jag vill söka i. Med länet utvalt får jag däremot noll träffar. Torde ha något att göra med vad br.form har för värden på sina olika attribut, men vad?

br.select_form(name="mainform")

dagens_org_nr = str(br.find_control("uss")) #här går vi "bakvägen" genom att extrahera strängen som innehåller samtliga org-nr för bolag med kunggörelser i dag.
#print br.form
dagens_org_nr=dagens_org_nr[30:-15] #en enda lång sträng med de orgnr som har kunggörelser i dag. Denna sträng stoppar vi tillbaka i formuläret lite längre ner.
print "dagens org_nr:"+dagens_org_nr
print "längd dagens org nr:" + str(len(dagens_org_nr))

print br
#print response7.read()

response8 = br.follow_link(text="F\xf6retag")
#print br

br.select_form(name="mainform")
print "mainform, rad 129"
print br.form
#br.form.find_control("limit").readonly = False #sätt till False så att vi kan ändra värdet
#br.form["limit"] = ["250"] #så att vi får alla träffar på en lång lista
#print br.form
br.form["orgnr"]=dagens_org_nr #här stoppar vi tillbaka strängen med de org_nr som har kunggörelser i dag. 
br.form["lan[]"]=["12"] #Ange samtidigt skåne som län för att bara få dem från skåne.
print "före submit"
print br.form

response9 = br.submit() #nu har vi en lista på de bolag som har kunggörelser i dag och säte i skåne. Kruxet är att de bara visas 25 i taget. (22 maj)
#print response9.read()

br.select_form(name="mainform")
print "efter submit"
print br.form
br.form.find_control("limit").readonly = False #sätt till False så att vi kan ändra värdet
br.form.find_control("end").readonly = False
br.form["limit"] = "250" #så att vi får alla träffar på en lång lista
br.form["end"]= "250"
print "ny version av formen"
print br.form

respone9b = br.submit()

br.select_form(name="mainform")
print "efter andra submit" #PROBLEM: Den checkbox-control som heter orgnrs[] och som vi vill använda för att extrahera listan på organisationsnummer i skåne försvinner när vi kör en andra submit. (24 maj)
print br.form

#print br.form.find_control("orgnrs[]").items[0]
dagens_skanska_orgnr = br.form.find_control("orgnrs[]").items[:]   #detta ger en lista på org_nr för skånska bolag som har kunggörelser det akutella datumet
print "antal org_nr: " + str(len(dagens_skanska_orgnr))
#print str(dagens_skanska_orgnr[0])+"detta är listan: "+str(dagens_skanska_orgnr[1])
#print br.form["orgnrs[]"]

for d in range(len(dagens_skanska_orgnr)):

    br.open("http://www.allabolag.se", timeout=300.0)
    print br

    br.select_form(name="f_search")
    #print br.form
    br["what"]=str(dagens_skanska_orgnr[d])
    response10=br.submit()#26 april: so far, so good. Nästa steg blir att skrapa upp den info om bolaget vi vill ha, främst verksamhet, omsättning och, via bolagsveket, vad kunggörelsen gäller.
    #print "rad 159"
    #print response10.read()
    #print list(br.links())
    root = lxml.html.fromstring(response10.read())
    namn = root.cssselect("td.reportTitle h1")[0] 
    namn = namn.text_content()
    #print type(namn)
    namn= namn.encode('utf-8') #namn har typen ElementUnicodeResult. Detta konverterar det till en sträng
    #print type(namn)
    print namn


    oms = root.cssselect("tr.bgLightPink td")
    print oms[14].text_content()

    br.back()

    br.select_form(name="f_search")
    br["what"]=namn
    response11 = br.submit()

    #print response11.read()

    root = lxml.html.fromstring(response11.read())
    print root.cssselect("td.text11grey6 span") #här verkar det bli fel ibland, dvs. listan som returneras är tom. Varför? 22 maj 2013
    if len(root.cssselect("td.text11grey6 span"))>1:

        verksamhet = root.cssselect("td.text11grey6 span")[1]
        verksamhet =  verksamhet.tail
    else:
        verksamhet = "Verksamhet ej funnen"    
    
    print verksamhet
    #for c in range(7):
    #    print oms[c].text_content()

    #response11= br.follow_link(text="Verksamhet & Status")  

    #verksamhet = root.cssselect("div.reportFrame a.linkOne")
    #for c in range(len(verksamhet)):
    #    print verksamhet[c].text_content()

    br.open("https://sokarende.bolagsverket.se/mia/", timeout=300.0) #undersök vad kunggörelsen handlar om hos Bolagsveket
    br.select_form(name="arende-sok-form")
    print br.form

    br["arende-sok-form:sokterm"]=str(dagens_skanska_orgnr[d])
    response12=br.submit()
    #print response12.read(

    root = lxml.html.fromstring(response12.read())
    arende_lista = root.cssselect("dl.orginfo li")

    #print "length " + str(len(arende_lista)) 

    for c in range(len(arende_lista)):
        print arende_lista[c].text

    arenden =[0,0,0,0,0]
    for c in range(5):
        if c<len(arende_lista):
            arenden[c]=arende_lista[c].text
        else:
            arenden[c]="-"
    #arenden[0:2]=arende_lista
    print arenden[0]
    print arenden[4]
    #arenden[0:len(arende_lista)]=arenden_lista

    scraperwiki.sqlite.save(unique_keys=["row"], data={"row":d, "name":namn, "oms":oms[14].text_content(), "verksamhet": verksamhet, "regarding":arenden[0], "regardingtwo":arenden[1], "regardingthree":arenden[2]}) 

    #for c in range(len(arende_lista)):
    #    if c>4:
    #        break
    #    else:
    #        scraperwiki.sqlite.save(unique_keys=["row"], data={"row":radnr, "name":namn, "pris":pris[h].text})    
    # print arende_lista[c].text


