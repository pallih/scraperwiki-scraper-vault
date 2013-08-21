import scraperwiki
import lxml.html
import re

html = scraperwiki.scrape("http://www.nhs.uk/ServiceDirectories/Pages/AcuteTrustListing.aspx")     
root = lxml.html.fromstring(html)
for tr in root.cssselect(".trust-list li a"):
    href = tr.attrib['href'].decode()
    contacts_href = href.replace('Overview','ContactDetails')
    print "Contacts href made: " + contacts_href

    # Only scrape the contact links, skip # links
    if (contacts_href.startswith('/Services/')):
        contactshtml = scraperwiki.scrape("http://www.nhs.uk/" + contacts_href)
        contactsroot = lxml.html.fromstring(contactshtml)

        trust_name = contactsroot.cssselect("h1#org-title")[0].text

        # Extract a telephone number if present
        tel_el = contactsroot.cssselect("div.panel.box.contact-details .panel-content .pad.clear div.col p")
        tel = ""
        try:
            #print tel_el[1].text_content()
            matchObj = re.search( r'Tel: ([\d\s()]+)', tel_el[1].text_content(), re.M|re.I)
            if matchObj:
                tel = matchObj.group(1)
                tel = tel.replace('(', '')
                tel = tel.replace(')', '')
        except:
            tel = ""

        # Extract the trust website
        web_el = contactsroot.cssselect("div.panel-content div.pad.clear p a")
        try:
            website = web_el[0].attrib['href'].decode()
        except:
            website = ""

        # Extract the trust postcode
        postcode_el = contactsroot.cssselect("h1#org-title")[0].getnext()
        postcode_txt = postcode_el.text_content()
        matchObj = re.search( r'.*,([\s\w]+)Website', postcode_txt, re.M|re.I)
        if matchObj:
            postcode_txt = matchObj.group(1)
        else:
            postcode_txt = ""
        postcode_txt = scraperwiki.geo.extract_gb_postcode(postcode_txt)

        if postcode_txt != '':
            latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode_txt)

        if latlng == None:
            print "LatLng failed for " + postcode_txt 
            latlng = [0,0]

        data = {
            'name': trust_name,
            'trust-url': website,
            'tel': tel,
            'postcode': postcode_txt,
            'lat': latlng[0],
            'lng': latlng[1]
            }
        print data
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
