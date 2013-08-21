import scraperwiki
import lxml.html
import re

html = scraperwiki.scrape("http://www.nhs.uk/ServiceDirectories/Pages/AcuteTrustListing.aspx")     
root = lxml.html.fromstring(html)
for tr in root.cssselect(".trust-list li a"):
    href = tr.attrib['href'].decode()
    contacts_href = href.replace('Overview','ContactDetails')
    hospAndClinics_href = href.replace('Overview','HospitalsAndClinics')

    # Only scrape the contact links, skip # links
    if (contacts_href.startswith('/Services/')):
        contactshtml = scraperwiki.scrape("http://www.nhs.uk/" + contacts_href)
        contactsroot = lxml.html.fromstring(contactshtml)

        trust_name = contactsroot.cssselect("h1#org-title")[0].text

        # Extract a telephone number if present
        tel_el = contactsroot.cssselect("div.panel.box.contact-details .panel-content .pad.clear div.col p")
        trust_tel = ""
        try:
            matchObj = re.search( r'Tel: ([\d\s()]+)', tel_el[1].text_content(), re.M|re.I)
            if matchObj:
                trust_tel = matchObj.group(1)
                trust_tel = trust_tel.replace('(', '')
                trust_tel = trust_tel.replace(')', '')
        except:
            trust_tel = ""

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

        # Get the list of hospitals
        hospAndClinics_html = scraperwiki.scrape("http://www.nhs.uk/" + hospAndClinics_href)
        hospAndClinics_root = lxml.html.fromstring(hospAndClinics_html)
        hosplist_div = hospAndClinics_root.cssselect("div.hospital-list div.panel div.panel-content")
        
        for hosp in hosplist_div:
            hosp_name = hosp.cssselect("a")[0].text
            hosp_detail_url = hosp.cssselect("a")[0].attrib['href'].decode()
            hosp_contact_dt = hosp.cssselect("dl dt");
            hosp_contact_dd = hosp.cssselect("dl dd");
            
            try:
                hosp_tel = hosp_contact_dd[1].text
            except:
                hosp_tel = ""

            # The address is within the dd but <br /> seperated. Hence needs this constuct
            hosp_address = ""
            for node in hosp_contact_dd[0].xpath('node()'):
                if getattr(node, 'tag', None) == None:
                    hosp_address += node + '\n'
            hosp_address = hosp_address.rstrip('\n')     # remove trail \n from above

            hosp_postcode_txt = scraperwiki.geo.extract_gb_postcode(hosp_address.split('\n')[-1] )
            if hosp_postcode_txt != '':
                latlng = scraperwiki.geo.gb_postcode_to_latlng(hosp_postcode_txt)
            if latlng == None:
                print "LatLng failed for " + hosp_postcode_txt 
                latlng = [0,0]

            data = {
                'name': hosp_name,
                'address': hosp_address,
                'postcode': hosp_postcode_txt,
                'tel': hosp_tel,
                'lat': latlng[0],
                'lng': latlng[1],
                'trust_name': trust_name,
                'trust_url': website,
                'trust_tel': trust_tel,
                'trust_postcode': postcode_txt
                }
            print data
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)
