import scraperwiki

# Blank Python
# Det här är en hårdkådad version för att hämta hem alla ideon-bolag på Ideons egen sida. Obs! Koden skulle behöva generaliseras och snyggas till. Kruxet är dock att jag inte vet hur man välja och vrakar bland de länkar i listan som [l for l in br.links()] ger (2012-05-12).

import lxml.html

from mechanize import Browser

#list with links to pages where companies are listed:
Pages =["http://www.ideon.se/foeretag/ideonfoeretag", 
"http://www.ideon.se/foeretag/ideonfoeretag/?tx_dfideontoolbox_pi2[cat1]=1&tx_dfideontoolbox_pi2[cat2]=0&tx_dfideontoolbox_pi2[cat3]=0&tx_dfideontoolbox_pi2[pointer]=1&tx_dfideontoolbox_pi2[mode]=1",
"http://www.ideon.se/foeretag/ideonfoeretag/?tx_dfideontoolbox_pi2[cat1]=1&tx_dfideontoolbox_pi2[cat2]=0&tx_dfideontoolbox_pi2[cat3]=0&tx_dfideontoolbox_pi2[pointer]=2&tx_dfideontoolbox_pi2[mode]=1", 
"http://www.ideon.se/foeretag/ideonfoeretag/?tx_dfideontoolbox_pi2[cat1]=1&tx_dfideontoolbox_pi2[cat2]=0&tx_dfideontoolbox_pi2[cat3]=0&tx_dfideontoolbox_pi2[pointer]=3&tx_dfideontoolbox_pi2[mode]=1",
"http://www.ideon.se/foeretag/ideonfoeretag/?tx_dfideontoolbox_pi2[cat1]=1&tx_dfideontoolbox_pi2[cat2]=0&tx_dfideontoolbox_pi2[cat3]=0&tx_dfideontoolbox_pi2[pointer]=4&tx_dfideontoolbox_pi2[mode]=1", 
"http://www.ideon.se/foeretag/ideonfoeretag/?tx_dfideontoolbox_pi2[cat1]=1&tx_dfideontoolbox_pi2[cat2]=0&tx_dfideontoolbox_pi2[cat3]=0&tx_dfideontoolbox_pi2[pointer]=5&tx_dfideontoolbox_pi2[mode]=1"]

Pages_inkubator = "http://www.ideon.se/foeretag/inkubatorfoeretag/"
#f = open("Ideonbolag.txt", "w")

br = Browser()
br2 = Browser()
br.set_handle_robots(False) #ignorera robots.txt
br2.set_handle_robots(False)

count = 0

#for c in range(len(Pages_inkubator)) :
for c in range(1):
    br.open(Pages_inkubator, timeout=300.0)
    print br 
    print c   
    nice_links = [l for l in br.links()] #returns list of  all links on page

    #print nice_links
    b=23 #ignorera de första länkarna, som inte är till bolag.


    for link in nice_links:
        b=b+1
        #print "hit kom jag", b
        #print nice_links[b]
        response = br.follow_link(nice_links[b])

        #print response.read()
        root= lxml.html.fromstring(response.read())

    
        if root.cssselect("div.tx-dfideontoolbox-pi2-singleView h1"):
            tr = root.cssselect("div.tx-dfideontoolbox-pi2-singleView h1")[0]
            Bolagsnamn = tr.text
            print Bolagsnamn 
   
            if root.cssselect("td.tx-dfideontoolbox-pi2-singleViewField-user-details"):
    
                td = root.cssselect("td.tx-dfideontoolbox-pi2-singleViewField-user-details")[0]
        
                beskrivning = td.text
            else:
                beskrivning = "Ingen beskrivning"

            if root.cssselect("td.tx-dfideontoolbox-pi2-singleViewField-org_no"):
                td2 = root.cssselect("td.tx-dfideontoolbox-pi2-singleViewField-org_no")[0]
                next = td2.getnext()
                
                #hämta adress och styrelseledamöter för aktuellt bolag:
            
                br2.open("http://www.allabolag.se", timeout=300.0)
            
            
                br2.select_form(name="f_search")
            
                if (len(next.text)==11):        
                    br2["what"]=next.text #fyll i bolagets organisationsnummer
                    response2=br2.submit()
                    #print "hit kom jag"
                    #print response.read()

                    root2 = lxml.html.fromstring(response2.read())
                    td_list = root2.cssselect("div#printContent td")
                    #for c in range(20):
                    #    print td_list[c].text

            
                    try:
                        adress = td_list[14].text + td_list[15].text
                    except:
                        adress = "out of range"
            
                
                    try:
                        response3 = br2.follow_link(text_regex='Befattningshavare')
               
                              
                        #print "hit kom jag"   
            
                        root3 = lxml.html.fromstring(response3.read())
                        for befattningshavare in root3.cssselect("a.linkOne"):
                        
                            count = count +1
                            namn = befattningshavare.text_content()
                            titel = befattningshavare.tail
                            row = {'Nr' : count, 'Bolag' : Bolagsnamn, 'Befattningshavare' : namn, 'Titel' : titel}
                            scraperwiki.sqlite.save(unique_keys=["Nr"], data=row)                       
                    except:
                        print "Link not found for: ", tr.text, "Organisationsnr: ", next.text
                
                   #print befattningshavare.getnext()            
                else:
                    print "Felaktigt organisationsnummer för ", tr.text, ": ", next.text

            #slut på sekvens för att hämta adress och styrelseledamöter för aktuellt bolag        



            else:
                print "Inget organisationsnummer för: ", Bolagsnamn 
            #print tr.text, next.text, beskrivning
        
                        
            #row = {'Nr' : count, 'Bolag' : tr.text, 'Organisationsnummer' : next.text, 'Beskrivning' : beskrivning}
            #scraperwiki.sqlite.save(unique_keys=["Nr"], data=row)
            #print scraperwiki.sqlite.show_tables() 
            
                

        else:
            print "End of list"
            break #we have reached end of list of companies on page. Move on to the next page.



import scraperwiki

# Blank Python
# Det här är en hårdkådad version för att hämta hem alla ideon-bolag på Ideons egen sida. Obs! Koden skulle behöva generaliseras och snyggas till. Kruxet är dock att jag inte vet hur man välja och vrakar bland de länkar i listan som [l for l in br.links()] ger (2012-05-12).

import lxml.html

from mechanize import Browser

#list with links to pages where companies are listed:
Pages =["http://www.ideon.se/foeretag/ideonfoeretag", 
"http://www.ideon.se/foeretag/ideonfoeretag/?tx_dfideontoolbox_pi2[cat1]=1&tx_dfideontoolbox_pi2[cat2]=0&tx_dfideontoolbox_pi2[cat3]=0&tx_dfideontoolbox_pi2[pointer]=1&tx_dfideontoolbox_pi2[mode]=1",
"http://www.ideon.se/foeretag/ideonfoeretag/?tx_dfideontoolbox_pi2[cat1]=1&tx_dfideontoolbox_pi2[cat2]=0&tx_dfideontoolbox_pi2[cat3]=0&tx_dfideontoolbox_pi2[pointer]=2&tx_dfideontoolbox_pi2[mode]=1", 
"http://www.ideon.se/foeretag/ideonfoeretag/?tx_dfideontoolbox_pi2[cat1]=1&tx_dfideontoolbox_pi2[cat2]=0&tx_dfideontoolbox_pi2[cat3]=0&tx_dfideontoolbox_pi2[pointer]=3&tx_dfideontoolbox_pi2[mode]=1",
"http://www.ideon.se/foeretag/ideonfoeretag/?tx_dfideontoolbox_pi2[cat1]=1&tx_dfideontoolbox_pi2[cat2]=0&tx_dfideontoolbox_pi2[cat3]=0&tx_dfideontoolbox_pi2[pointer]=4&tx_dfideontoolbox_pi2[mode]=1", 
"http://www.ideon.se/foeretag/ideonfoeretag/?tx_dfideontoolbox_pi2[cat1]=1&tx_dfideontoolbox_pi2[cat2]=0&tx_dfideontoolbox_pi2[cat3]=0&tx_dfideontoolbox_pi2[pointer]=5&tx_dfideontoolbox_pi2[mode]=1"]

Pages_inkubator = "http://www.ideon.se/foeretag/inkubatorfoeretag/"
#f = open("Ideonbolag.txt", "w")

br = Browser()
br2 = Browser()
br.set_handle_robots(False) #ignorera robots.txt
br2.set_handle_robots(False)

count = 0

#for c in range(len(Pages_inkubator)) :
for c in range(1):
    br.open(Pages_inkubator, timeout=300.0)
    print br 
    print c   
    nice_links = [l for l in br.links()] #returns list of  all links on page

    #print nice_links
    b=23 #ignorera de första länkarna, som inte är till bolag.


    for link in nice_links:
        b=b+1
        #print "hit kom jag", b
        #print nice_links[b]
        response = br.follow_link(nice_links[b])

        #print response.read()
        root= lxml.html.fromstring(response.read())

    
        if root.cssselect("div.tx-dfideontoolbox-pi2-singleView h1"):
            tr = root.cssselect("div.tx-dfideontoolbox-pi2-singleView h1")[0]
            Bolagsnamn = tr.text
            print Bolagsnamn 
   
            if root.cssselect("td.tx-dfideontoolbox-pi2-singleViewField-user-details"):
    
                td = root.cssselect("td.tx-dfideontoolbox-pi2-singleViewField-user-details")[0]
        
                beskrivning = td.text
            else:
                beskrivning = "Ingen beskrivning"

            if root.cssselect("td.tx-dfideontoolbox-pi2-singleViewField-org_no"):
                td2 = root.cssselect("td.tx-dfideontoolbox-pi2-singleViewField-org_no")[0]
                next = td2.getnext()
                
                #hämta adress och styrelseledamöter för aktuellt bolag:
            
                br2.open("http://www.allabolag.se", timeout=300.0)
            
            
                br2.select_form(name="f_search")
            
                if (len(next.text)==11):        
                    br2["what"]=next.text #fyll i bolagets organisationsnummer
                    response2=br2.submit()
                    #print "hit kom jag"
                    #print response.read()

                    root2 = lxml.html.fromstring(response2.read())
                    td_list = root2.cssselect("div#printContent td")
                    #for c in range(20):
                    #    print td_list[c].text

            
                    try:
                        adress = td_list[14].text + td_list[15].text
                    except:
                        adress = "out of range"
            
                
                    try:
                        response3 = br2.follow_link(text_regex='Befattningshavare')
               
                              
                        #print "hit kom jag"   
            
                        root3 = lxml.html.fromstring(response3.read())
                        for befattningshavare in root3.cssselect("a.linkOne"):
                        
                            count = count +1
                            namn = befattningshavare.text_content()
                            titel = befattningshavare.tail
                            row = {'Nr' : count, 'Bolag' : Bolagsnamn, 'Befattningshavare' : namn, 'Titel' : titel}
                            scraperwiki.sqlite.save(unique_keys=["Nr"], data=row)                       
                    except:
                        print "Link not found for: ", tr.text, "Organisationsnr: ", next.text
                
                   #print befattningshavare.getnext()            
                else:
                    print "Felaktigt organisationsnummer för ", tr.text, ": ", next.text

            #slut på sekvens för att hämta adress och styrelseledamöter för aktuellt bolag        



            else:
                print "Inget organisationsnummer för: ", Bolagsnamn 
            #print tr.text, next.text, beskrivning
        
                        
            #row = {'Nr' : count, 'Bolag' : tr.text, 'Organisationsnummer' : next.text, 'Beskrivning' : beskrivning}
            #scraperwiki.sqlite.save(unique_keys=["Nr"], data=row)
            #print scraperwiki.sqlite.show_tables() 
            
                

        else:
            print "End of list"
            break #we have reached end of list of companies on page. Move on to the next page.



