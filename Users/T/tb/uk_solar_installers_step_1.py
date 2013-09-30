import lxml.html
import scraperwiki

page_link = "http://www.microgenerationcertification.org/mcs-consumer/installer-search.php?searchPaginationPage=" #searchRegionID=1442&

def esp(s, d="="): # return last substring of string s with delimiter d
    return (s[::-1].split(d)[0][::-1])

for page in xrange(120, 385):
    #print "\nPAGE",page,page_link+str(page)
    html = scraperwiki.scrape(page_link+str(page))
    root = lxml.html.fromstring(html)
    table = root.cssselect("table.mcsResultsTable")[0][1]
    for tr in table: #root.cssselect("table.mcsResultsTable"):
        tds = tr.cssselect("a")
        name = tds[0].text
        link = tds[0].attrib['href']
        id = int(esp(link))
        data = { 'id':id, 'name':name }
        #print data
        details_link = "http://www.microgenerationcertification.org/mcs-consumer/installer-profile.php?ID="
        details_html = scraperwiki.scrape(details_link+str(id))
        details_root = lxml.html.fromstring(details_html)
        details_table = details_root.cssselect("div.mcsColumnsTwoOne")

        details_as_list_of_text = [x.text for x in details_table[0]]

        #Add static fields
        record = { "name":details_as_list_of_text[0] }
        if len(details_as_list_of_text) > 4: record["address"] = details_as_list_of_text[4]

        #Add dynamic fields
        fields = { "Certificate Number":"cert_num",
                   "Date Certified":"cert_date",
                   "Telephone":"phone",
                   "Website":"website",
                   "Email":"email",
                   "Contact":"contact",
                   "Contact Position":"contact_position" }
        
        for field in details_as_list_of_text:
            key = field.split(":")[0]
            #print "KEY IS", key
            if key in fields:
                cleaned_up = field[len(key)+1:]
                cleaned_up = cleaned_up.strip()
                #print "~~~", key, ">>>", cleaned_up
                if len(cleaned_up) > 0:
                    record[fields[key]] = cleaned_up
        
        print "RECORD:", record

        scraperwiki.sqlite.save(unique_keys=['name'], data=record)


import lxml.html
import scraperwiki

page_link = "http://www.microgenerationcertification.org/mcs-consumer/installer-search.php?searchPaginationPage=" #searchRegionID=1442&

def esp(s, d="="): # return last substring of string s with delimiter d
    return (s[::-1].split(d)[0][::-1])

for page in xrange(120, 385):
    #print "\nPAGE",page,page_link+str(page)
    html = scraperwiki.scrape(page_link+str(page))
    root = lxml.html.fromstring(html)
    table = root.cssselect("table.mcsResultsTable")[0][1]
    for tr in table: #root.cssselect("table.mcsResultsTable"):
        tds = tr.cssselect("a")
        name = tds[0].text
        link = tds[0].attrib['href']
        id = int(esp(link))
        data = { 'id':id, 'name':name }
        #print data
        details_link = "http://www.microgenerationcertification.org/mcs-consumer/installer-profile.php?ID="
        details_html = scraperwiki.scrape(details_link+str(id))
        details_root = lxml.html.fromstring(details_html)
        details_table = details_root.cssselect("div.mcsColumnsTwoOne")

        details_as_list_of_text = [x.text for x in details_table[0]]

        #Add static fields
        record = { "name":details_as_list_of_text[0] }
        if len(details_as_list_of_text) > 4: record["address"] = details_as_list_of_text[4]

        #Add dynamic fields
        fields = { "Certificate Number":"cert_num",
                   "Date Certified":"cert_date",
                   "Telephone":"phone",
                   "Website":"website",
                   "Email":"email",
                   "Contact":"contact",
                   "Contact Position":"contact_position" }
        
        for field in details_as_list_of_text:
            key = field.split(":")[0]
            #print "KEY IS", key
            if key in fields:
                cleaned_up = field[len(key)+1:]
                cleaned_up = cleaned_up.strip()
                #print "~~~", key, ">>>", cleaned_up
                if len(cleaned_up) > 0:
                    record[fields[key]] = cleaned_up
        
        print "RECORD:", record

        scraperwiki.sqlite.save(unique_keys=['name'], data=record)


