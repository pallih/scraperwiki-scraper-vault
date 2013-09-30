import scraperwiki

from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

scraperwiki.sqlite.attach("dfid-contracts_1") # Attaching scraper https://scraperwiki.com/scrapers/dfid-contracts_1/

# Use LIMIT 2800 to skip the first 2800 results (if it breaks).
links = scraperwiki.sqlite.select("URL from `dfid-contracts_1`.swdata LIMIT 13790, 500000") # Selecting the URLs collected from the search results from contract finder

# Getting the html from the links
for link in links:
    url = link["URL"]
    print url
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #print soup
    
    if soup.find("h2", "legend-edit") is not None:

        title = soup.find("h2", "legend-edit").get_text().replace("English", "").strip()
        
        # Paragraph tags contain information like reference, duration, nature of contract, etc.
        ps = soup.find_all("p", "clearfix")

        length = 'NaN'
        value = 'NaN'
        location = 'NaN'
        organisation = 'NaN'
        framework = 'NaN'
        date= 'NaN'
        nature  = 'NaN'
        

        for p in ps:
            span_text = ""
            span = p.find("span")
            if span: 
                span_text = span.get_text().strip()
                span.clear()
            if span_text != "":
                info = p.get_text().strip()
                
                #print span_text
                #print p.get_text().strip()
                #print
    
                if span_text == "Reference number:":
                    ref = info
                    #print ref
    
                elif span_text == "Estimated length of contract:":
                    #print info
                    length = info
                    #print value

                elif span_text == "Awarded value":
                    #print info
                    value = int(info.encode("utf8").replace(",","").replace("£",""))
                    #print value
    
                elif span_text == "Location where the contract is to be carried out:":
                    #print info
                    location = info.replace("English","")
                    #print location
    
                elif span_text == "Name of the buying organisation:":
                    organisation = info.replace("English","")
                    #print organisation
    
                elif span_text == "Is it a framework agreement?":
                    framework = info
                    #print framework
              
                elif span_text == "Awarded on:":
                    date = info
                    #print date
    
                elif span_text == "Nature of procurement":
                    nature = info
                    #print nature
    
        classification_details = soup.find("span", id = "pagecontent_0_ctlNoticeClassificationDetails_ctl00_lblClassificationName")
    
        if classification_details is not None:
            classification = classification_details.get_text()
        
            description_details = soup.find("div", "inner expanded-content")
            description = description_details.get_text().replace("English","").strip()
        
            # If a contract contains multiple suppliers but "multiple/NA" in the relevant fields otherwise extract the relevant fields
            suppliers_details = soup.find_all("div", "field-container border-top")
            if suppliers_details is not None:
                if len(suppliers_details) > 1:
                    supplier_name = "multiple"
                    supplier_address = "multiple"
                    supplier_amount = "NA"
                    supplier_contracting = "NA"
                else:
                    suppliers_details = soup.find("div", "field-container border-top")
                    if suppliers_details is not None:
                        supplier_name_address = suppliers_details.find("div", "col-left")
                        
                        supplier_name_address_spans = supplier_name_address.find_all("span")    
                        supplier_name = supplier_name_address_spans[0].get_text()
                        supplier_address = supplier_name_address_spans[1].get_text().strip()
                
                        if supplier_address != "" and supplier_address[0] == ",":
                            #print supplier_address[2:]
                            supplier_address = supplier_address[2:]
                
                        supplier_amount_contracting = suppliers_details.find("div", "col-right")
                        supplier_amount_contracting_spans = supplier_amount_contracting.find_all("span", id == True)
                        supplier_amount = supplier_amount_contracting_spans[1].get_text()
                        supplier_contracting = supplier_amount_contracting_spans[3].get_text()
            
                        # Save data to ScraperWiki database, saving unique title and URL
                        data = {"Title": title, "URL": url, "Reference": ref, "Duration": length, "Value": value, "Location": location, "Organisation": organisation, "Framework": framework, "Date": date, "Nature": nature, "Classification": classification, "Description": description, "Supplier_Name": supplier_name, "Supplier_Address": supplier_address, "Supplier_Amount": supplier_amount, "Supplier_Contracting": supplier_contracting }
                        scraperwiki.sqlite.save(["URL", "Title"], data)import scraperwiki

from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

scraperwiki.sqlite.attach("dfid-contracts_1") # Attaching scraper https://scraperwiki.com/scrapers/dfid-contracts_1/

# Use LIMIT 2800 to skip the first 2800 results (if it breaks).
links = scraperwiki.sqlite.select("URL from `dfid-contracts_1`.swdata LIMIT 13790, 500000") # Selecting the URLs collected from the search results from contract finder

# Getting the html from the links
for link in links:
    url = link["URL"]
    print url
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #print soup
    
    if soup.find("h2", "legend-edit") is not None:

        title = soup.find("h2", "legend-edit").get_text().replace("English", "").strip()
        
        # Paragraph tags contain information like reference, duration, nature of contract, etc.
        ps = soup.find_all("p", "clearfix")

        length = 'NaN'
        value = 'NaN'
        location = 'NaN'
        organisation = 'NaN'
        framework = 'NaN'
        date= 'NaN'
        nature  = 'NaN'
        

        for p in ps:
            span_text = ""
            span = p.find("span")
            if span: 
                span_text = span.get_text().strip()
                span.clear()
            if span_text != "":
                info = p.get_text().strip()
                
                #print span_text
                #print p.get_text().strip()
                #print
    
                if span_text == "Reference number:":
                    ref = info
                    #print ref
    
                elif span_text == "Estimated length of contract:":
                    #print info
                    length = info
                    #print value

                elif span_text == "Awarded value":
                    #print info
                    value = int(info.encode("utf8").replace(",","").replace("£",""))
                    #print value
    
                elif span_text == "Location where the contract is to be carried out:":
                    #print info
                    location = info.replace("English","")
                    #print location
    
                elif span_text == "Name of the buying organisation:":
                    organisation = info.replace("English","")
                    #print organisation
    
                elif span_text == "Is it a framework agreement?":
                    framework = info
                    #print framework
              
                elif span_text == "Awarded on:":
                    date = info
                    #print date
    
                elif span_text == "Nature of procurement":
                    nature = info
                    #print nature
    
        classification_details = soup.find("span", id = "pagecontent_0_ctlNoticeClassificationDetails_ctl00_lblClassificationName")
    
        if classification_details is not None:
            classification = classification_details.get_text()
        
            description_details = soup.find("div", "inner expanded-content")
            description = description_details.get_text().replace("English","").strip()
        
            # If a contract contains multiple suppliers but "multiple/NA" in the relevant fields otherwise extract the relevant fields
            suppliers_details = soup.find_all("div", "field-container border-top")
            if suppliers_details is not None:
                if len(suppliers_details) > 1:
                    supplier_name = "multiple"
                    supplier_address = "multiple"
                    supplier_amount = "NA"
                    supplier_contracting = "NA"
                else:
                    suppliers_details = soup.find("div", "field-container border-top")
                    if suppliers_details is not None:
                        supplier_name_address = suppliers_details.find("div", "col-left")
                        
                        supplier_name_address_spans = supplier_name_address.find_all("span")    
                        supplier_name = supplier_name_address_spans[0].get_text()
                        supplier_address = supplier_name_address_spans[1].get_text().strip()
                
                        if supplier_address != "" and supplier_address[0] == ",":
                            #print supplier_address[2:]
                            supplier_address = supplier_address[2:]
                
                        supplier_amount_contracting = suppliers_details.find("div", "col-right")
                        supplier_amount_contracting_spans = supplier_amount_contracting.find_all("span", id == True)
                        supplier_amount = supplier_amount_contracting_spans[1].get_text()
                        supplier_contracting = supplier_amount_contracting_spans[3].get_text()
            
                        # Save data to ScraperWiki database, saving unique title and URL
                        data = {"Title": title, "URL": url, "Reference": ref, "Duration": length, "Value": value, "Location": location, "Organisation": organisation, "Framework": framework, "Date": date, "Nature": nature, "Classification": classification, "Description": description, "Supplier_Name": supplier_name, "Supplier_Address": supplier_address, "Supplier_Amount": supplier_amount, "Supplier_Contracting": supplier_contracting }
                        scraperwiki.sqlite.save(["URL", "Title"], data)