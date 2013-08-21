import scraperwiki
import lxml.html

url = "http://www.parliament.uk/mps-lords-and-offices/mps/"

html = scraperwiki.scrape(url) # get the webpage

root= lxml.html.fromstring(html) # transform the webpage so we can work with it

table=root.cssselect("table")[1] # find the second table (0 is the first one)

rows=table.cssselect("tbody tr") # find every row in the table

for row in rows:
    # for each row do the following
    content=row.cssselect("td") # find column data

    if len(content)>1:
        # only process if both columns are present..,
        constituency=content[1].text_content() # constituency is the second column
        (last,first_party)=content[0].text_content().split(",") # process the first column, first name is seperated from the rest by comma
        (first,party)=first_party.split(" (") # seperat last name and party (seperated by ' (')
        party=party.replace(")","") # remove the parentheses from the party
        mep={"first":first,
            "last":last,
            "party":party,
            "constituency":constituency,
            "unique":"%s-%s-%s"%(first,last,party)} # construct an entry for the mep
        scraperwiki.sqlite.save(unique_keys=["unique"],data=mep) # save the entry
