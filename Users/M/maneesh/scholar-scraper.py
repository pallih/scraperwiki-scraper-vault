###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

def scrape_titlepagesection(section):
    fieldNames = section.cssselect("div.cit-dt");
    fieldValues = section.cssselect("div.cit-dd");
#    print len(fieldNames), ", ", len(fieldValues);

    record = {};

    for i in range(len(fieldNames)):
        field = fieldNames[i].text;
        value = fieldValues[i].text;


        # Pain to deal with capturing the full description/abstract since requires dealing with <br> tags. Punt for now.
        # We only scrape first line of description/abstract.
#        for j in range(0,len(fieldValues[i])): 
#             print j, ", ", (fieldValues[i][j]).text; 
#            value = value + fieldValues[i][j].text

        if not value:
            aNodes = fieldValues[i].cssselect("a");
            imgNodes = fieldValues[i].cssselect("img");
            if aNodes:
                value = aNodes[0].text;
            elif imgNodes:
                value = imgNodes[0].attrib.get('src');
        
#        print field, ", ", value;
        record[field] = value;

        # Convert the chart URL to data values (move to sepearate function later
        if (field == 'Citations per year'):
            cpyURL = value;
            (cpyLeftURL,cpyRightURL) = cpyURL.split('&chxr=1,');
            (yRange,cpyRightURL) = cpyRightURL.split('&chd=t:');
            (dataVals,yearVals) = cpyRightURL.split('&chxl=0:|');
            
            yRangeArray = yRange.split(',');
            for j in range(len(yRangeArray)):
                yRangeArray[j] = int(yRangeArray[j]);
#            print yRange, yRangeArray;
            record['CitCountRange'] = yRangeArray;
            
            dataValsArray = dataVals.split(',');
            for j in range(len(dataValsArray)):
                dataValsArray[j] = float(dataValsArray[j]);
#            print dataVals, dataValsArray;
            record['CitCountData'] = dataValsArray; 
            
            yearValsArray = yearVals.split('|');
            firstYear = int(yearValsArray[0]);  #Should error check that yearValsArray[0] holds a year
            for j in range(len(yearValsArray)):
                yearValsArray[j] = firstYear + j;
#            print yearVals, yearValsArray;
            record['CitCountYears'] = yearValsArray;

#    print record;
    return record;

def scrape_titlepage(title_url):
    titlepagehtml = scraperwiki.scrape(title_url);
#    print titlepagehtml;
    titlepageroot = lxml.html.fromstring(titlepagehtml);
    fieldbox = titlepageroot.cssselect("div.g-section.cit-fieldbox");
#    print fieldbox;
#    print len(fieldbox);

    #Scrape main sectoin with title, authors, etc.
    main_sec = fieldbox[0];
    mainRecord = scrape_titlepagesection(main_sec);


    # Scrape the citations per year chart url
    chart_sec = fieldbox[1];
    chartRecord = scrape_titlepagesection(chart_sec);

    record = {};
    record.update(mainRecord);
    record.update(chartRecord.items());
#    print "TitleRecord:", record;
    return record;


# Scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    global globrank;

    cit_table = root.cssselect("table.cit-table");
#    print cit_table;
    rows = cit_table[0].cssselect("tr.cit-table.item");
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        record['Rank'] = globrank;
        globrank += 1;
        table_cells = row.cssselect("td")
        if table_cells:

#            select = table_cells[0];    # Will be None in all cases.
#            record['Select'] = select.text;
            
            title = table_cells[1].cssselect("a");
            if title:
                record['Title'] = title[0].text;
                print "Paper ", globrank, ": ", record['Title'];
                title_url = urlparse.urljoin(base_url, title[0].attrib.get('href'));
#                print title_url;
                titlepageRecord = scrape_titlepage(title_url);
                record.update(titlepageRecord);
            
            citedBy = table_cells[2].cssselect("a");
            if citedBy:
                record['CitedBy'] = citedBy[0].text;
            else:
                record['CitedBy'] = 0;
            
            asterisk = table_cells[3].cssselect("span");
            if asterisk:
                record['Asterisk'] = True;
            else:
                record['Asterisk'] = False;

            year = table_cells[4].text;
            if year:
                record['Year'] = table_cells[4].text;
            else:
                record['Year'] = 0;

#            # Print out the data we've gathered
            print record;
            # Finally, save the record to the datastore - 'Artist' is our unique key
#            scraperwiki.datastore.save(['Title'], record)
            scraperwiki.sqlite.save(['Rank'], record);
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    print url;
    html = scraperwiki.scrape(url)
#    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    dark_links = root.cssselect("a.cit-dark-link")
    next_found = False;
    for link in dark_links:
        if (link.text == 'Next >'):
#            print link.text;
            next_link = link;
            next_found = True;
    if next_found:
#        print next_link.attrib.get('href');
        next_url = urlparse.urljoin(base_url, next_link.attrib.get('href'))
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://scholar.google.com/'
startIdx = 0;
globrank = 1;
remainder_url = 'citations?hl=en&user=YPzKczYAAAAJ&pagesize=100&view_op=list_works&cstart=' + str(startIdx);
starting_url = urlparse.urljoin(base_url, remainder_url)
scrape_and_look_for_next_link(starting_url)
