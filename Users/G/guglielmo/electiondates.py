import scraperwiki
import mechanize
import lxml.html           

br = mechanize.Browser()
br.set_handle_robots(False)   
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

minint_url = "http://elezionistorico.interno.it/index.php?tpel=G"
response = br.open(minint_url)

date_links = br.links(url_regex='tpel=G&dtel=.*')
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
    br.open(br.click_link(url_regex='tpel=G&dtel=.*&tpa=I', nr=0))

    reg_links = {}
    for l in br.links(url_regex='tpel=G&dtel=.*&tpa=I&tpe=R'):
        reg_links[l.text] = l.url

    sorted_regions = reversed(sorted(reg_links.iterkeys()))
    for reg in sorted_regions:
        print " Regione: %s" % reg
        br.open(reg_links[reg])

        prov_links = {}
        for l in br.links(url_regex='tpel=G&dtel=.*&tpa=I&tpe=P'):
            prov_links[l.text] = l.url

        sorted_provinces = reversed(sorted(prov_links.iterkeys()))
        for prov in sorted_provinces:
            print "  Provincia: %s" % prov
            br.open(prov_links[prov])

            root = lxml.html.fromstring(br.response().read())
            divs = root.cssselect("div.sezione_panel")
            for div in divs:
                if div.text == 'Comune':
                    links = div.getnext().cssselect('ul li a')
                    for link in links:
                        city = ''
                        for word in link.text.split():
                            city = city + ' ' + word
                        data = {
                          'election_date': el_date,
                          'reg': reg,
                          'prov' : prov,
                          'city' : city,
                        }
                        scraperwiki.sqlite.save(unique_keys=['election_date', 'reg', 'prov', 'city'], data=data)
                        print "    %s" % (city, )
import scraperwiki
import mechanize
import lxml.html           

br = mechanize.Browser()
br.set_handle_robots(False)   
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

minint_url = "http://elezionistorico.interno.it/index.php?tpel=G"
response = br.open(minint_url)

date_links = br.links(url_regex='tpel=G&dtel=.*')
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
    br.open(br.click_link(url_regex='tpel=G&dtel=.*&tpa=I', nr=0))

    reg_links = {}
    for l in br.links(url_regex='tpel=G&dtel=.*&tpa=I&tpe=R'):
        reg_links[l.text] = l.url

    sorted_regions = reversed(sorted(reg_links.iterkeys()))
    for reg in sorted_regions:
        print " Regione: %s" % reg
        br.open(reg_links[reg])

        prov_links = {}
        for l in br.links(url_regex='tpel=G&dtel=.*&tpa=I&tpe=P'):
            prov_links[l.text] = l.url

        sorted_provinces = reversed(sorted(prov_links.iterkeys()))
        for prov in sorted_provinces:
            print "  Provincia: %s" % prov
            br.open(prov_links[prov])

            root = lxml.html.fromstring(br.response().read())
            divs = root.cssselect("div.sezione_panel")
            for div in divs:
                if div.text == 'Comune':
                    links = div.getnext().cssselect('ul li a')
                    for link in links:
                        city = ''
                        for word in link.text.split():
                            city = city + ' ' + word
                        data = {
                          'election_date': el_date,
                          'reg': reg,
                          'prov' : prov,
                          'city' : city,
                        }
                        scraperwiki.sqlite.save(unique_keys=['election_date', 'reg', 'prov', 'city'], data=data)
                        print "    %s" % (city, )
