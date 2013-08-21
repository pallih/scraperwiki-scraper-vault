import scraperwiki
import simplejson
import urllib2
import lxml.html

not_given = "keine Angabe"
#NUM_PAGES = 5
#for page in range(1, NUM_PAGES+1):
base_url = 'http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/Schulportrait.aspx?IDSchulzweig='
# 8566
for n in range(8566, 11400):
    url = base_url + str(n)
    print url
    try:
        result_html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(result_html)
        for el in root.cssselect("div.portrait_rechts"):
            #print lxml.html.tostring(el)
            schoolname = el.cssselect("span.MySchulName")[0]
            if schoolname.text is None:
                print "no school found"
            else: 
                data = {}
                data['id'] = schoolname.text[-5:]
                data['Name'] = schoolname.text
                scraperwiki.sqlite.execute("select url from swdata where id = "+schoolname.text[-5:])
                data['url'] = url
                schooltype = el.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblSchulart")[0]
                data['Type'] = schooltype.text
                schoolstreet = el.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblStrasse")[0]
                data['Street'] = schoolstreet.text
                schooladdress = el.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblOrt")[0]
                if schooladdress.text is None:
                    data['Address'] = "keine Angabe"
                    data['District'] = "keine Angabe"
                else: 
                    data['Address'] = schooladdress.text
                    district = schooladdress.text.split("(")[1].split(")")[0].strip()
                    data['District'] = district
                schooltel = el.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblTelefon")[0]
                if schooltel.text is None:
                    data['Tel'] = "keine Angabe"
                else:
                    data['Tel'] = schooltel.text
                schoolfax = el.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblFax")[0]
                if schoolfax.text is not None:
                    data['Fax'] = schoolfax.text
                else:
                    data['Fax'] = "keine Angabe"
                schoolmail = el.cssselect("#ctl00_ContentPlaceHolderMenuListe_HLinkEMail")[0]
                if schoolmail.text is not None:
                    data['Mail'] = schoolmail.text
                else:
                    data['Mail'] = "keine Angabe"
                schoolweb = el.cssselect("#ctl00_ContentPlaceHolderMenuListe_HLinkWeb")[0]
                if schoolweb.text is not None:
                    data['Web'] = schoolweb.text
                else:
                    data['Web'] = "keine Angabe"
                schoolchef = el.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblLeitung")[0]
                if schoolchef.text is not None:
                    data['Chef'] = schoolchef.text
                else: 
                    data['Chef'] = "keine Angabe"
                for schoollang in root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblSprachen"):
                    #print schoollang.text
                    if schoollang.text is not None:
                        data['Lang'] = schoollang.text
                    else:
                        data['Lang'] = "keine Angabe"
                for schoolother in root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblAngebote"):
                    if schoolfax.text is not None:
                        data['Other'] = schoolother.text
                    else:
                        data['Other'] = "keine Angabe"
                for schoolopen in root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblZusatz"):
                    if schoolfax.text is not None:
                        data['Addition'] = schoolopen.text
                    else:
                        data['Addition'] = "keine Angabe"
                scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
    
