import scraperwiki
import lxml.html
import re


#Get and store statistics data from the IDMC summary page
def scrapeSummary():

    countrydata = {}
    url = "http://www.internal-displacement.org/8025708F004CE90B/%28httpPages%29/22FB1D4E2B196DAA802570BB005E787C?OpenDocument&count=1000"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    #Get every tr in the table whose class is "stats_table"
    trs = root.cssselect('div.stats_table tr')

    #Get table headings
    headings = []
    ths = trs[0].cssselect('th')
    for j in range(len(ths)):
        heading = ths[j].text.strip()
        heading = re.sub('-', ' to ', heading)
        heading = re.sub('%', ' percent ', heading)
        heading = re.sub(r'[^a-zA-Z0-9 ]', '', heading)
        headings += [heading]
        print("Heading: " + headings[j])

    #Get table contents
    for i in range(1,len(trs)):
        
        #Ignore spacers between data rows
        if len(trs[i]) == 1 or trs[i][0].text == None:
            continue
        
        #Grab 1 row of data
        country = trs[i][0].text.strip().encode('utf8')
        print("Country: " + country)
        countrydata[country] = {}
        for j in range(len(trs[i])):
            countrydata[country][headings[j]] = trs[i][j].text

        #Create id that won't crash the sqlite save
        #Replace % with percent and strip out nonalphanumeric characters
        #or the data name will crash the sqlite save code
        countrykey = re.sub(r'[^a-zA-Z0-9 ]','', country)
        countrydata[country]['key'] = countrykey
            
        #Save results to the scraperwiki summary table
        scraperwiki.sqlite.save(unique_keys=['key'], table_name='summary', data=countrydata[country])

    return(countrydata)



#Main code block

countrydata = scrapeSummary()

import scraperwiki
import lxml.html
import re


#Get and store statistics data from the IDMC summary page
def scrapeSummary():

    countrydata = {}
    url = "http://www.internal-displacement.org/8025708F004CE90B/%28httpPages%29/22FB1D4E2B196DAA802570BB005E787C?OpenDocument&count=1000"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    #Get every tr in the table whose class is "stats_table"
    trs = root.cssselect('div.stats_table tr')

    #Get table headings
    headings = []
    ths = trs[0].cssselect('th')
    for j in range(len(ths)):
        heading = ths[j].text.strip()
        heading = re.sub('-', ' to ', heading)
        heading = re.sub('%', ' percent ', heading)
        heading = re.sub(r'[^a-zA-Z0-9 ]', '', heading)
        headings += [heading]
        print("Heading: " + headings[j])

    #Get table contents
    for i in range(1,len(trs)):
        
        #Ignore spacers between data rows
        if len(trs[i]) == 1 or trs[i][0].text == None:
            continue
        
        #Grab 1 row of data
        country = trs[i][0].text.strip().encode('utf8')
        print("Country: " + country)
        countrydata[country] = {}
        for j in range(len(trs[i])):
            countrydata[country][headings[j]] = trs[i][j].text

        #Create id that won't crash the sqlite save
        #Replace % with percent and strip out nonalphanumeric characters
        #or the data name will crash the sqlite save code
        countrykey = re.sub(r'[^a-zA-Z0-9 ]','', country)
        countrydata[country]['key'] = countrykey
            
        #Save results to the scraperwiki summary table
        scraperwiki.sqlite.save(unique_keys=['key'], table_name='summary', data=countrydata[country])

    return(countrydata)



#Main code block

countrydata = scrapeSummary()

