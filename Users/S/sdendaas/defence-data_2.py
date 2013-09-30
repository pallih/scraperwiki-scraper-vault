import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("defence-contracts-all")

scrapings = scraperwiki.sqlite.select("* from 'defence-contracts-all'.swdata")

for scraping in scrapings:
    url = scraping["URL"]
    #print url

    soup = BeautifulSoup(scraping["HTML"])

    title = soup.find("div", "fieldset-title corners-top").get_text().replace("English", "").strip()
    #print title

# I want you to get me the info in the first paragraph of information in the contract!!!

# Reference number
# Estimated length of contract
# Awarded value
# Location where the contract is to be carried out:
# Name of the buying organisation:



    ps = soup.find_all("p", "clearfix") # The paragraphs we're interested in have the id "clearfix"
    for p in ps:
        print p
        span_text = ""
        span = p.find("span")
        if span: 
            span_text = span.get_text().strip() # Text in the spans have the column headings
            span.clear()
        if span_text != "":
            info = p.get_text().strip() # The rest of the text in the ps have the column values


            if span_text == "Reference number:":
                ref = info
                #print ref

            elif span_text == "Estimated length of contract:":
                length = info
                #print length

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
                d = info
                date = d[6:] + "-" + d[3:5] + "-" + d[:2] # Making the format YY-MM-DD for MySQL
                #print date

            elif span_text == "Nature of procurement":
                nature = info
                #print nature
    
    data = {"URL":url, "Title":title, "Reference":ref, "Duration":length, "Value":value, "Location":location, "Organisation":organisation, "Framework":framework, "Date":date, "Nature":nature}
    scraperwiki.sqlite.save(["URL"], data)



    



import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("defence-contracts-all")

scrapings = scraperwiki.sqlite.select("* from 'defence-contracts-all'.swdata")

for scraping in scrapings:
    url = scraping["URL"]
    #print url

    soup = BeautifulSoup(scraping["HTML"])

    title = soup.find("div", "fieldset-title corners-top").get_text().replace("English", "").strip()
    #print title

# I want you to get me the info in the first paragraph of information in the contract!!!

# Reference number
# Estimated length of contract
# Awarded value
# Location where the contract is to be carried out:
# Name of the buying organisation:



    ps = soup.find_all("p", "clearfix") # The paragraphs we're interested in have the id "clearfix"
    for p in ps:
        print p
        span_text = ""
        span = p.find("span")
        if span: 
            span_text = span.get_text().strip() # Text in the spans have the column headings
            span.clear()
        if span_text != "":
            info = p.get_text().strip() # The rest of the text in the ps have the column values


            if span_text == "Reference number:":
                ref = info
                #print ref

            elif span_text == "Estimated length of contract:":
                length = info
                #print length

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
                d = info
                date = d[6:] + "-" + d[3:5] + "-" + d[:2] # Making the format YY-MM-DD for MySQL
                #print date

            elif span_text == "Nature of procurement":
                nature = info
                #print nature
    
    data = {"URL":url, "Title":title, "Reference":ref, "Duration":length, "Value":value, "Location":location, "Organisation":organisation, "Framework":framework, "Date":date, "Nature":nature}
    scraperwiki.sqlite.save(["URL"], data)



    



