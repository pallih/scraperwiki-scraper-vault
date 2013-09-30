import scraperwiki, lxml.html, time
import re

csv = scraperwiki.scrape('http://analyzethis.net/ticker1.csv')
tickers = csv.splitlines()



deets_regex = re.compile('(.*)(\d+\d+)(.*)')  # Magic regex to match name, age, role later on..

for ticker in tickers:

    company_url = 'http://finance.yahoo.com/q/pr?s=%s+Profile' % ticker
    html = scraperwiki.scrape(company_url)
    print company_url
    time.sleep(2)
    dom = lxml.html.fromstring(html)
    if dom.cssselect('.time_rtq_ticker'):        #there is company info on this page! let's scrape it

        data = {}
        # You can build cssselect with a hierarchy, but need to remember ..
        #  normal tags appear with their name, classes prepended with . and ids prepended with #
        data['CompanyName'] = dom.cssselect('.yfi_rt_quote_summary .hd .title h2')[0].text_content()

        # Grabs that table with the data in it
        table = dom.cssselect('.yfnc_datamodoutline1')[0]

        # Iterates over the rows in the table
        for row in table.cssselect('tr'):
            # If there is more than one column
            if len(row) > 1: 
                key = row[0].text_content()  # First TD
                value = row[1].text_content() # Second TD

                # Write the value straight into a dictionary (for saving).
                if key == "Index Membership:":
                    data['Index'] = value
                elif key == "Sector:":
                    data['Sector'] = value
                elif key == "Industry:":
                    data['Industry'] = value
                elif key == "Full Time Employees:":
                    data['Employees'] = value

        co = data['CompanyName']
        data['Ticker'] = co[co.find('(')+1:co.rfind(')')].strip()
        data['CompanyName'] = co[:co.find('(')].strip()

        data['Ticker Price'] = dom.cssselect('.time_rtq_ticker')[0].text_content()

        # This is where you'd call scraperwiki.sqlite.save().  It might make sense
        # to save this, and then save the executives in a separate table, but referencing this
        # one by name 
        scraperwiki.sqlite.save(['CompanyName'], data, table_name='companies')
        #print data

        # Executive .. Make sure we get the table on the right hand side by choosing the 
        # .yfnc_datamodoutline1 inside .yfnc_modtitlew2 and pulling the first table from that.
#        table = dom.cssselect('.yfnc_modtitlew2 .yfnc_datamodoutline1 table')[0]
#        for row in table[1:]:    # Skip the first row of headers
#           detailed = row[0].text_content()  # Because we have extra markup here.
#           pay = row[1].text
#           exercised = row[1].text

            # Get the useful details out of the blob of data from the first column
#           detailed = " ".join(detailed.split()) # Remove trailing and duplicate spaces
#           m = deets_regex.match(detailed)
#           if m:
#               name = m.groups(0)[0].strip()
#               name = name[:-1].strip()  # strip the trailing comma that I missed because I couldn\t remember the regex
#               age = m.groups(0)[1].strip()
#               roles = m.groups(0)[2].strip()
#           else:
               # We'll be missing the age, but it does make it easier to find details
#               name,roles = detailed.strip().split(",")
#               age = "unknown"
#               print name, roles, age

            # Can now save name, age, roles, pay, and exercised..


                

#         print 'Sector:', dom.cssselect('.')[0].text
#         print 'Industry:', dom.cssselect('.yfnc_tabledata1')[2].text
#         print 'Employees:', dom.cssselect('.yfnc_tabledata1')[3].text
#         print 'Share Price: $', dom.cssselect('.time_rtq_ticker span')[0].text
    else:
        print 'Invalid ticker symbol! Visit URL for more info.'



import scraperwiki, lxml.html, time
import re

csv = scraperwiki.scrape('http://analyzethis.net/ticker1.csv')
tickers = csv.splitlines()



deets_regex = re.compile('(.*)(\d+\d+)(.*)')  # Magic regex to match name, age, role later on..

for ticker in tickers:

    company_url = 'http://finance.yahoo.com/q/pr?s=%s+Profile' % ticker
    html = scraperwiki.scrape(company_url)
    print company_url
    time.sleep(2)
    dom = lxml.html.fromstring(html)
    if dom.cssselect('.time_rtq_ticker'):        #there is company info on this page! let's scrape it

        data = {}
        # You can build cssselect with a hierarchy, but need to remember ..
        #  normal tags appear with their name, classes prepended with . and ids prepended with #
        data['CompanyName'] = dom.cssselect('.yfi_rt_quote_summary .hd .title h2')[0].text_content()

        # Grabs that table with the data in it
        table = dom.cssselect('.yfnc_datamodoutline1')[0]

        # Iterates over the rows in the table
        for row in table.cssselect('tr'):
            # If there is more than one column
            if len(row) > 1: 
                key = row[0].text_content()  # First TD
                value = row[1].text_content() # Second TD

                # Write the value straight into a dictionary (for saving).
                if key == "Index Membership:":
                    data['Index'] = value
                elif key == "Sector:":
                    data['Sector'] = value
                elif key == "Industry:":
                    data['Industry'] = value
                elif key == "Full Time Employees:":
                    data['Employees'] = value

        co = data['CompanyName']
        data['Ticker'] = co[co.find('(')+1:co.rfind(')')].strip()
        data['CompanyName'] = co[:co.find('(')].strip()

        data['Ticker Price'] = dom.cssselect('.time_rtq_ticker')[0].text_content()

        # This is where you'd call scraperwiki.sqlite.save().  It might make sense
        # to save this, and then save the executives in a separate table, but referencing this
        # one by name 
        scraperwiki.sqlite.save(['CompanyName'], data, table_name='companies')
        #print data

        # Executive .. Make sure we get the table on the right hand side by choosing the 
        # .yfnc_datamodoutline1 inside .yfnc_modtitlew2 and pulling the first table from that.
#        table = dom.cssselect('.yfnc_modtitlew2 .yfnc_datamodoutline1 table')[0]
#        for row in table[1:]:    # Skip the first row of headers
#           detailed = row[0].text_content()  # Because we have extra markup here.
#           pay = row[1].text
#           exercised = row[1].text

            # Get the useful details out of the blob of data from the first column
#           detailed = " ".join(detailed.split()) # Remove trailing and duplicate spaces
#           m = deets_regex.match(detailed)
#           if m:
#               name = m.groups(0)[0].strip()
#               name = name[:-1].strip()  # strip the trailing comma that I missed because I couldn\t remember the regex
#               age = m.groups(0)[1].strip()
#               roles = m.groups(0)[2].strip()
#           else:
               # We'll be missing the age, but it does make it easier to find details
#               name,roles = detailed.strip().split(",")
#               age = "unknown"
#               print name, roles, age

            # Can now save name, age, roles, pay, and exercised..


                

#         print 'Sector:', dom.cssselect('.')[0].text
#         print 'Industry:', dom.cssselect('.yfnc_tabledata1')[2].text
#         print 'Employees:', dom.cssselect('.yfnc_tabledata1')[3].text
#         print 'Share Price: $', dom.cssselect('.time_rtq_ticker span')[0].text
    else:
        print 'Invalid ticker symbol! Visit URL for more info.'



