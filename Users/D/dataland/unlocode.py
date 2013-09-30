import scraperwiki
import lxml.html
import urllib
import datetime

# Step 1, Get Reference Data
base_url = "http://www.unece.org/fileadmin/DAM/cefact/locode/Service/LocodeColumn.htm"
html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)
for count, tr in enumerate(root.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    # Change Indicator Reference Values
    if count <= 5:
        now = datetime.datetime.now()
        data = {"tmsp_scraped":str(now), "chg_code":row[0].strip(), "chg_code_desc":row[1].strip()}
        scraperwiki.sqlite.save(unique_keys=["chg_code"], data=data, table_name="smtb_chg_code")
    # Function Reference Values
    elif count >10 and count <=19:
        now = datetime.datetime.now()
        data = {"tmsp_scraped":str(now), "func_code":row[0].strip(), "func_code_desc":row[1].strip()}
        scraperwiki.sqlite.save(unique_keys=["func_code"], data=data, table_name="smtb_func_code")
    # Status Reference Values
    elif count >=20 and count <=30:
        now = datetime.datetime.now()
        data = {"tmsp_scraped":str(now), "status_code":row[0].strip(), "status_code_desc":row[1].strip()}
        scraperwiki.sqlite.save(unique_keys=["status_code"], data=data, table_name="smtb_status_code")

# Step 2, Get Subdivision Reference Data
sd_url = "http://www.unece.org/cefact/locode/subdivisions.html"
base_url = "http://www.unece.org/fileadmin/DAM/cefact/locode/Subdivision/"
sdhtml = scraperwiki.scrape(sd_url)
sdroot = lxml.html.fromstring(sdhtml)
for count, tr in enumerate(sdroot.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    if len(row)>0:
        final_url = base_url + row[0].lower() + "Sub.htm"
        fnhtml = scraperwiki.scrape(final_url)
        fnroot = lxml.html.fromstring(fnhtml)
        for count2, tr in enumerate(fnroot.cssselect('tr')):
            row2 = [td.text_content() for td in tr.cssselect('td')]
            if len(row2)==4:
                if row2[0]!="Country ":
                    now = datetime.datetime.now()
                    data = {"tmsp_scraped":str(now), "country_code":row2[0].strip(), "subdivision":row2[1].strip(), "subdivision_name":row2[2].strip(), "subdivision_level":row2[3].strip()}
                    scraperwiki.sqlite.save(unique_keys=["country_code","subdivision"], data=data, table_name="smtb_subdivision")

# Step 3, Loop through country code index page
index_url = 'http://www.unece.org/cefact/locode/service/location.html'
base_url = 'http://www.unece.org/fileadmin/DAM/cefact/locode/'
indhtml = scraperwiki.scrape(index_url)
indroot = lxml.html.fromstring(indhtml)
for count, tr in enumerate(indroot.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    if len(row)>0:
        # Step 4, Scrape page for specific country code
        final_url = base_url + row[0].lower() + ".htm"
        fnhtml = scraperwiki.scrape(final_url)
        fnroot = lxml.html.fromstring(fnhtml)
        for count3, tr in enumerate(fnroot.cssselect('tr')):
            row3 = [td.text_content() for td in tr.cssselect('td')]
            if len(row3)==11 and row3[1]!="LOCODE":
                if row3[5][:1] == '1':
                    port_flag = 'Y'
                    now = datetime.datetime.now()
                    data = {"tmsp_scraped":str(now), "ch_flag":row3[0].strip(), "locode":row3[1].strip(), "name":row3[2].strip(), "name_wo_diacritics":row3[3].strip(),
                            "subdiv":row3[4].strip(), "function":row3[5].strip(), "status":row3[6].strip(), "date":row3[7].strip(), "iata":row3[8].strip(), "coordinates":row3[9],
                            "remarks":row3[10].strip(), "port_flag":port_flag.strip()}
                    scraperwiki.sqlite.save(unique_keys=["locode"], data=data, table_name="s_locode")                                                    import scraperwiki
import lxml.html
import urllib
import datetime

# Step 1, Get Reference Data
base_url = "http://www.unece.org/fileadmin/DAM/cefact/locode/Service/LocodeColumn.htm"
html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)
for count, tr in enumerate(root.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    # Change Indicator Reference Values
    if count <= 5:
        now = datetime.datetime.now()
        data = {"tmsp_scraped":str(now), "chg_code":row[0].strip(), "chg_code_desc":row[1].strip()}
        scraperwiki.sqlite.save(unique_keys=["chg_code"], data=data, table_name="smtb_chg_code")
    # Function Reference Values
    elif count >10 and count <=19:
        now = datetime.datetime.now()
        data = {"tmsp_scraped":str(now), "func_code":row[0].strip(), "func_code_desc":row[1].strip()}
        scraperwiki.sqlite.save(unique_keys=["func_code"], data=data, table_name="smtb_func_code")
    # Status Reference Values
    elif count >=20 and count <=30:
        now = datetime.datetime.now()
        data = {"tmsp_scraped":str(now), "status_code":row[0].strip(), "status_code_desc":row[1].strip()}
        scraperwiki.sqlite.save(unique_keys=["status_code"], data=data, table_name="smtb_status_code")

# Step 2, Get Subdivision Reference Data
sd_url = "http://www.unece.org/cefact/locode/subdivisions.html"
base_url = "http://www.unece.org/fileadmin/DAM/cefact/locode/Subdivision/"
sdhtml = scraperwiki.scrape(sd_url)
sdroot = lxml.html.fromstring(sdhtml)
for count, tr in enumerate(sdroot.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    if len(row)>0:
        final_url = base_url + row[0].lower() + "Sub.htm"
        fnhtml = scraperwiki.scrape(final_url)
        fnroot = lxml.html.fromstring(fnhtml)
        for count2, tr in enumerate(fnroot.cssselect('tr')):
            row2 = [td.text_content() for td in tr.cssselect('td')]
            if len(row2)==4:
                if row2[0]!="Country ":
                    now = datetime.datetime.now()
                    data = {"tmsp_scraped":str(now), "country_code":row2[0].strip(), "subdivision":row2[1].strip(), "subdivision_name":row2[2].strip(), "subdivision_level":row2[3].strip()}
                    scraperwiki.sqlite.save(unique_keys=["country_code","subdivision"], data=data, table_name="smtb_subdivision")

# Step 3, Loop through country code index page
index_url = 'http://www.unece.org/cefact/locode/service/location.html'
base_url = 'http://www.unece.org/fileadmin/DAM/cefact/locode/'
indhtml = scraperwiki.scrape(index_url)
indroot = lxml.html.fromstring(indhtml)
for count, tr in enumerate(indroot.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    if len(row)>0:
        # Step 4, Scrape page for specific country code
        final_url = base_url + row[0].lower() + ".htm"
        fnhtml = scraperwiki.scrape(final_url)
        fnroot = lxml.html.fromstring(fnhtml)
        for count3, tr in enumerate(fnroot.cssselect('tr')):
            row3 = [td.text_content() for td in tr.cssselect('td')]
            if len(row3)==11 and row3[1]!="LOCODE":
                if row3[5][:1] == '1':
                    port_flag = 'Y'
                    now = datetime.datetime.now()
                    data = {"tmsp_scraped":str(now), "ch_flag":row3[0].strip(), "locode":row3[1].strip(), "name":row3[2].strip(), "name_wo_diacritics":row3[3].strip(),
                            "subdiv":row3[4].strip(), "function":row3[5].strip(), "status":row3[6].strip(), "date":row3[7].strip(), "iata":row3[8].strip(), "coordinates":row3[9],
                            "remarks":row3[10].strip(), "port_flag":port_flag.strip()}
                    scraperwiki.sqlite.save(unique_keys=["locode"], data=data, table_name="s_locode")                                                    