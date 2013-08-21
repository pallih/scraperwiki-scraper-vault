import scraperwiki
from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

#attach your previous scraper which collected the source code of the individual pages (use the name shown in the scraperwiki URL!)
scraperwiki.sqlite.attach("pageextract")
#select the database that contains the source code of all of the pages
scrapings = scraperwiki.sqlite.select("* from 'pageextract'.swdata")

#print the urls so that you can see what url your code breaks on if it does

for scraping in scrapings:
    url = scraping["url"]
    print url

#select html source code from the database and make it searchable with beautifulsoup
#extract information of interest and clean up a bit
    soup = BeautifulSoup(scraping["html"])
#OLD code:    title = soup.find("div", "fieldset-title corners-top").get_text().replace("English", "").strip()
    title = soup.find("h2", "legend-edit").get_text().replace("English", "").strip()
# title is to be found in the h2 tag of id "legend-edit". Need to get rid of the "English"

# Paragraph tags contain information like reference, duration, nature of contract, etc.
#search for p tags
    ps = soup.find_all("p","clearfix") # The paragraphs we're interested in have the id "clearfix"

    for p in ps:
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

