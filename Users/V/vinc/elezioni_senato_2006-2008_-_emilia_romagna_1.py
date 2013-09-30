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
        br.open(area_links[area])

        reg_links = {}
        for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=R'):
            reg_links[l.text] = l.url
            
        sorted_reg = reversed(sorted(reg_links.iterkeys()))
        for reg in sorted_reg:
            if reg == 'LAZIO':
                print "  Regione: %s" % reg
                br.open(reg_links[reg])

            
                prov_links = {}
                for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=P'):
                    prov_links[l.text] = l.url

                sorted_prov = reversed(sorted(prov_links.iterkeys()))
                for prov in sorted_prov:
                    print "  Provincia: %s" % prov
                    br.open(prov_links[prov])    

                    com_links = {}
                    for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=C'):
                        com_links[l.text] = l.url

                    sorted_com = reversed(sorted(com_links.iterkeys()))
                    for com in sorted_com:
                        print "  Comune: %s" % com
                        br.open(com_links[com]) 
            

                        root = lxml.html.fromstring(br.response().read())
                    

                        rows = root.cssselect("table.dati tr")[1:]


                        nome = ''
                        for row in rows:
                                          
                            ths= row.cssselect('th')
                            tds= row.cssselect('td')
                        
                            if len(tds) == 8:
                                nome = ths[0].text_content()                  
                            else:
                                data = {
                                        'date': el_date,
                                        'area': area,
                                        'reg' : reg,
                                        'prov' : prov,
                                        'com' : com,
                                        'candidate' : nome,
                                        'party' : ths[0].text_content(),   
                                        'votes' : tds[6].text_content(), 
                                        'perc' : tds[7].text_content(),                      
                                        }
                                scraperwiki.sqlite.save(unique_keys=['date', 'area', 'reg', 'prov', 'com', 'candidate', 'party', 'votes', 'perc'], data=data)
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
        br.open(area_links[area])

        reg_links = {}
        for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=R'):
            reg_links[l.text] = l.url
            
        sorted_reg = reversed(sorted(reg_links.iterkeys()))
        for reg in sorted_reg:
            if reg == 'LAZIO':
                print "  Regione: %s" % reg
                br.open(reg_links[reg])

            
                prov_links = {}
                for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=P'):
                    prov_links[l.text] = l.url

                sorted_prov = reversed(sorted(prov_links.iterkeys()))
                for prov in sorted_prov:
                    print "  Provincia: %s" % prov
                    br.open(prov_links[prov])    

                    com_links = {}
                    for l in br.links(url_regex='tpel=S&dtel=.*&tpa=I&tpe=C'):
                        com_links[l.text] = l.url

                    sorted_com = reversed(sorted(com_links.iterkeys()))
                    for com in sorted_com:
                        print "  Comune: %s" % com
                        br.open(com_links[com]) 
            

                        root = lxml.html.fromstring(br.response().read())
                    

                        rows = root.cssselect("table.dati tr")[1:]


                        nome = ''
                        for row in rows:
                                          
                            ths= row.cssselect('th')
                            tds= row.cssselect('td')
                        
                            if len(tds) == 8:
                                nome = ths[0].text_content()                  
                            else:
                                data = {
                                        'date': el_date,
                                        'area': area,
                                        'reg' : reg,
                                        'prov' : prov,
                                        'com' : com,
                                        'candidate' : nome,
                                        'party' : ths[0].text_content(),   
                                        'votes' : tds[6].text_content(), 
                                        'perc' : tds[7].text_content(),                      
                                        }
                                scraperwiki.sqlite.save(unique_keys=['date', 'area', 'reg', 'prov', 'com', 'candidate', 'party', 'votes', 'perc'], data=data)
