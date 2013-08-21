import scraperwiki
import lxml.html
import re


#Get list of countrynames and the address of their statistics pages, from UNICEF index page
def getCountryurls():

    countryurls = {}
    url = "http://www.unicef.org/statistics/index_countrystats.html"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    #Get every div whose class is contentrow. These are the countrynames
    #that UNICEF is active in
    #Grab every <a> tag. These link to "infobycountry/xxx.html"
    #xxx is the country url; xxx_statistics is its statistics page
    #Bangladesh and Jamaica have _stuff in their urls
    #Bangladesh statistics is at bangladesh_bangladesh_statistics.html
    #Jamaica statistics is as jamaica_statistics.html
    #Can't just ignore anything after a "_"
    #because of trinidad_tobago, sri_lanka, turks_caicos.
    #Some countrynames also have trailing spaces- strip() removes them.
    countries = root.cssselect('div.contentrow a')
    for i in range(len(countries)):
        #Handle blank countrynames - by ignoring them
        if countries[i].text == None:
            print("***couldn't process " + countries[i].attrib['href'][15:-5] + " country name")
            continue
        #print(str(i) + countries[i].text)
        countryname = countries[i].text.strip()

        #These countries don't have statistics pages
        if countryname == "Montserrat" or \
           countryname == "Hong Kong, Special Administrative Region, People's Republic of China" or \
           countryname == "Turks and Caicos Islands" or \
           countryname == "Montenegro" or \
           countryname == "British Virgin Islands" or \
           countryname == "Tokelau" or \
           countryname == "South Sudan, Republic of" or \
           countryname == "Kosovo under UNSC res. 1244": 
            continue

        #Strip special characters out of the country names
        if countryname == u"C\xf4te d' Ivoire": #FIXIT: Must be a better way of dealing with Cote d'Ivoire accent
            countryname = "Cote d'Ivoire"
        countryname = re.sub(r'[^a-zA-Z0-9 ]','', countryname) #Same problem as the stats data
        #Store the country data
        countryurls[countryname] = countries[i].attrib['href'][15:-5]+ "_statistics"

    countryurls['Angola']         = "angola_statistics"
    countryurls['Bangladesh']     = "bangladesh_bangladesh_statistics"
    countryurls['India']          = "india_statistics"
    countryurls['Jamaica']        = "jamaica_statistics"
    countryurls['Maldives']       = "maldives_maldives_statistics"
    countryurls['Nepal']          = "nepal_nepal_statistics"
    countryurls['Pakistan']       = "pakistan_pakistan_statistics"
    countryurls['Serbia']         = "serbia_11601"
    countryurls['United Kingdom'] = "uk_statistics"

    #Get every div whose class is contentrow_last. These are the countries
    #that UNICEF is not active in
    #Get all the <a> tags
    #The countries UNICEF isn't is have url issues too,
    #e.g. liechtenstein statistics are on page liechtenstein.html
    #Ditto bruneidarussalam.html, cyprus.html, malta.html,
    #mauritius.html, monaco.html, singapore.html, bahamas.html
    #Watch out for the _statistics in the address for Latvia, although
    #latvia.html also works.
    countries = root.cssselect('div.contentrow_last a')
    for i in range(len(countries)):
        if countries[i].text == None:
            print("***couldn't process " + countries[i].attrib['href'][15:-5])
            continue
        #print(str(i) + countries[i].text)

        countryname = countries[i].text.strip()

        #FIXIT: these countries' data pages aren't in standard format, and will need their own scrapers
        if countryname == "Cyprus":
            continue

        countryname = re.sub(r'[^a-zA-Z0-9 ]','', countryname) #Same problem as the stats data
        countryurls[countryname] = countries[i].attrib['href'][15:-5]

    return(countryurls)



#Get and store statistics data from a given UNICEF country statistics page
def getCountryStats(countryname, countryurl):

    print("Scraping statistics for " + countryname)
    
    #Get UNICEF page for a given country
    url = "http://www.unicef.org/infobycountry/" + countryurl + ".html"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    
    #Find all the data tables on the page. These have class statisticsn, if that's needed
    countrydata = {}
    tables = root.cssselect("table")
    for i in range(len(tables)):
    
        #All the data entries in each table are tagged with <p>
        ps = tables[i].cssselect("p")
    
        #The first entry is the table title. Use this as the datagroup title
        tableheading = ps[0].text
        countrydata[tableheading] = {}
        countrydata[tableheading]['country'] = countryname
    
        #Grab the rest of the data, which is in two columns:
        #lhs is data name, rhs is data value
        lhs = 1 #token for whether the input is on the lhs of the table
        dataname = ""
        for j in range(2,len(ps)):
            #None values crash the encode('utf8')
            if ps[j].text == None:
                cellvalue = ""
            else:
                cellvalue = ps[j].text.encode('utf8')
        
            if lhs == 1:
                #Replace % with percent and strip out nonalphanumeric characters
                #or the data name will crash the sqlite save code
                cellvalue = re.sub('-',' to ', cellvalue)
                cellvalue = re.sub('%',' percent ', cellvalue)
                cellvalue = re.sub(r'[^a-zA-Z0-9 ]','', cellvalue)
                dataname = cellvalue
            else:
                countrydata[tableheading][dataname] = cellvalue
            lhs = 1 - lhs
        
        #Save results to the scraperwiki table for this datagroup
        scraperwiki.sqlite.save(unique_keys=['country'], table_name=tableheading, data=countrydata[tableheading])

    return()


#Main code block

#countryurls = {}
#countryurls["Cyprus"] = "cyprus"
#countryurls["Haiti"] = "haiti_statistics"
#countryurls["Australia"] = "australia_statistics"

countryurls = getCountryurls()
for cname in countryurls:
    getCountryStats(cname, countryurls[cname])

