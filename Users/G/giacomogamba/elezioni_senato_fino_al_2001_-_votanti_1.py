# Scarica numero di elettori, votanti, percentuale votanti, schede bianche e schede nulle
# delle elezioni per il Senato dal 1948 al 2001.
# Dopo il 2001 la legge elettorale è cambiata, sostituendo i collegi (variabile col) con le province
# In questa versione scarichiamo tutte le Regioni.

import scraperwiki
import mechanize
import lxml.html           

br = mechanize.Browser()
br.set_handle_robots(False)   
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

minint_url = "http://elezionistorico.interno.it/index.php?tpel=S"
response = br.open(minint_url)

date_links = br.links(url_regex='tpel=S&dtel=.*')
elections_links = {}
for date_link in date_links:
    date_title = date_link.attrs[1][1]
    (day, month, year) = date_title.split('/')
    date_key = "%s-%s-%s" % (year, month, day)
    elections_links[date_key] = date_link.url

sorted_dates = reversed(sorted(elections_links.iterkeys()))
for el_date in sorted_dates:
    print "Data: %s" % el_date
    br.open(elections_links[el_date])

    # simulate click on Italia link in the right sidebar 
    br.open(br.click_link(url_regex='tpel=S&dtel=.*&tpa=I', nr=0))

    area_links = {}
    for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=A'):
        area_links[l.text] = l.url

    sorted_area = reversed(sorted(area_links.iterkeys()))
    for area in sorted_area:
        print " Area: %s" % area
        br.open(area_links[area]) # simulate click on Regione = Emilia Romagna

        reg_links = {}
        for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=R'):
            reg_links[l.text] = l.url
            
        sorted_reg = reversed(sorted(reg_links.iterkeys()))
        for reg in sorted_reg:
            
            print "  Regione: %s" % reg
            br.open(reg_links[reg]) # simulate click on Collegio

            
            col_links = {}
            for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=L'):
                col_links[l.text] = l.url

            sorted_col = reversed(sorted(col_links.iterkeys()))
            for col in sorted_col:
                print "  Collegio: %s" % col
                br.open(col_links[col])    # simulate click on Comune

                com_links = {}
                for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=C'):
                    com_links[l.text] = l.url

                sorted_com = reversed(sorted(com_links.iterkeys()))
                for com in sorted_com:
                    print "  Comune: %s" % com
                    br.open(com_links[com]) 
            

                    root = lxml.html.fromstring(br.response().read())
                    

                    rows = root.cssselect("table.dati_riepilogo tr")


                        
                    i=0
                    for row in rows:
                                          
                        tds= row.cssselect('td') # all data are within <td> </td> tags on the page
                        
                        if i == 0:
                            elettori = tds[0].text_content(), # for some reason these variables were returned as one-element tuples. 
                            votanti = tds[2].text_content(),  # We take only elements 0, 2, 4
                            perc = tds[4].text_content(),    
                            i=1                  
                        else:
                            bianche = tds[0].text_content(),
                            nulle = tds[2].text_content(), 
                            data = {                          # this is a dict containing all data for each Comune
                                'date': el_date,
                                'area': area.decode('latin1'), # string variables like area, reg, and col are applied to method decode ('latin1')
                                'reg' : reg.decode('latin1'),  # to read correctly accented vowels ("Forlì")
                                'collegio' : col.decode('latin1'),
                                'com' : com.decode('latin1'),
                                'elettori' : elettori[0],
                                'votanti' : votanti[0],   
                                'perc' : perc[0],
                                'bianche' : bianche[0],
                                'nulle' : nulle[0],                    
                                }
                            scraperwiki.sqlite.save(unique_keys=['date', 'area', 'reg', 'collegio', 'com', 'elettori', 'votanti', 'perc', 'bianche', 'nulle'], data=data)
