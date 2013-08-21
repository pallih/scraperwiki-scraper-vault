import lxml.html
import scraperwiki

html = scraperwiki.scrape("http://unstats.un.org/unsd/methods/m49/m49alpha.htm")

root = lxml.html.fromstring(html)

toptable = root.cssselect("div.Content td.content")
datatrs = toptable[0][6][0]

vals = ["","",""]
for i in range(1,len(datatrs)):
    
    #Ignore any data with just one array entry - i.e. Sudan
    if len(datatrs[i]) > 2:
    
        for j in range(3):
            if len(datatrs[i][j]) == 0:
                if datatrs[i][j].text == None:
                    vals[j] = "---"
                else:
                    vals[j] = datatrs[i][j].text.strip()
            else:
                if datatrs[i][j][0].text == None:
                    vals[j] = "---"
                else:
                    vals[j] = datatrs[i][j][0].text.strip()

            #Deal with spaces instead of values, e.g. for Sark's iso code
            if vals[j] == "":
                vals[j] = "---"
        
        newrow = {}
        newrow["UNstats code"] = vals[0]
        newrow["UNstats name"] = vals[1]
        newrow["ISO3166 code"] = vals[2]

        #Save to a scraperwiki table
        scraperwiki.sqlite.save(unique_keys=['UNstats name'], table_name="country codes", data=newrow)


#Save data for codes that were borked in the table
newrow = {}
newrow["UNstats code"] = "729"
newrow["UNstats name"] = "Sudan"
newrow["ISO3166 code"] = "SDN"
scraperwiki.sqlite.save(unique_keys=['UNstats name'], table_name="country codes", data=newrow)

