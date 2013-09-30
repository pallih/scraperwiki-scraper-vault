import scraperwiki

# max 1891157
for crno in range(130689, 1903573):
    crnostr = "%07d" % crno
    baseurl = "https://www.mobile-cr.gov.hk/mob/cps_criteria.do?queryCRNO="
    html = scraperwiki.scrape(baseurl + crnostr)

    import lxml.html           
    root = lxml.html.fromstring(html)

    tds = root.cssselect("tr td tr td")
    namestds = root.cssselect("td.data")   

    if tds == []:
        pass
    else:
        print tds[2].text_content()
        names = {}
        for namesno in range(len(namestds)):
            names["Name" + str(namesno)] = namestds[namesno].text_content()
        data = {
        'cr' : tds[1].text_content(),
        'English Company Name' : tds[2].text_content().rsplit('\r')[1].lstrip('\n\t'),
        'Chinese Company Name' : tds[2].text_content().rpartition('\r')[2].lstrip('\r\n\t'),
        'Company Type' : tds[4].text_content()[:-1],
        'Date of incorporation' : tds[6].text_content(),
        'Company status' : tds[8].text_content()[:-1],
        'Active status' : tds[10].text_content()[:-1],
        'Remarks' : tds[11].text_content()[16:],
        'Winding up mode' : tds[13].text_content()[:-1],
        'Date of Dissolution' : tds[15].text_content(),
        'Register of Charges' : tds[17].text_content()[:-1],
        'Important Note' : tds[18].text_content()[15:].lstrip('\r\n\t'),
        'Name History' : names
        }
        

    scraperwiki.sqlite.save(unique_keys=['cr'], data=data)
        
import scraperwiki

# max 1891157
for crno in range(130689, 1903573):
    crnostr = "%07d" % crno
    baseurl = "https://www.mobile-cr.gov.hk/mob/cps_criteria.do?queryCRNO="
    html = scraperwiki.scrape(baseurl + crnostr)

    import lxml.html           
    root = lxml.html.fromstring(html)

    tds = root.cssselect("tr td tr td")
    namestds = root.cssselect("td.data")   

    if tds == []:
        pass
    else:
        print tds[2].text_content()
        names = {}
        for namesno in range(len(namestds)):
            names["Name" + str(namesno)] = namestds[namesno].text_content()
        data = {
        'cr' : tds[1].text_content(),
        'English Company Name' : tds[2].text_content().rsplit('\r')[1].lstrip('\n\t'),
        'Chinese Company Name' : tds[2].text_content().rpartition('\r')[2].lstrip('\r\n\t'),
        'Company Type' : tds[4].text_content()[:-1],
        'Date of incorporation' : tds[6].text_content(),
        'Company status' : tds[8].text_content()[:-1],
        'Active status' : tds[10].text_content()[:-1],
        'Remarks' : tds[11].text_content()[16:],
        'Winding up mode' : tds[13].text_content()[:-1],
        'Date of Dissolution' : tds[15].text_content(),
        'Register of Charges' : tds[17].text_content()[:-1],
        'Important Note' : tds[18].text_content()[15:].lstrip('\r\n\t'),
        'Name History' : names
        }
        

    scraperwiki.sqlite.save(unique_keys=['cr'], data=data)
        
