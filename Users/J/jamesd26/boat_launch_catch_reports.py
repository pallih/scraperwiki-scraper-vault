#################################################################
### Description: This script returns catch reports from boat launches
### in Washington state along the Puget Sound and Peninsula.  There
### are two required inputs: a link to a wdfw catch report homepage
### and the desired number of records to be returned.


#################################################################
### Libraries
###

import scraperwiki
import lxml.html

#################################################################
### Script Follows
###

# Washington Department of Fish & Wildlife Website
website = "http://wdfw.wa.gov/fishing/creel/puget/2012/"

def extract_links(url, number_of_reports):
    '''
    Takes the link to a washington department fish and wildlife
    salmon catch homepage for a given year and the desired number
    of reports and returns the links to these individual report pages.
    '''
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    html_lst = []
    count = 0
    # links to individual catch reports are stored in the a tags of table rows
    for el in root.cssselect("tr a"):
        # the 103 index corresponds to the row containing data for the last week of
        # August, the end of the best time of year for salmon fishing in the Puget Sound.
        if count > 103 and count < (103+number_of_reports):
            html_catchreport =  el.attrib['href']
            # the extracted links are not the full link and need to be appended to the initial lin
            html2 = (url + html_catchreport)
            html_lst.append(html2)
        count += 1    
    return html_lst

def extract_data_from_reports(lst_of_url, number_of_records):
    '''
    Given a list of links to individual fishing reports from WDFW and the desired 
    number of reports return the following data: Date of Report, Site, Number of 
    Anglers, Number of Chinook caught, Number of Coho caught, Number of Pink Salmon 
    caught and lastly the Number of fish per angler.
    '''
    for url in lst_of_url:
        html = scraperwiki.scrape(url)
        root2 = lxml.html.fromstring(html)
        count = 0
        # Number of records to return from each link
        for i in range(number_of_records):
            tds = root2.cssselect("td")
            site = tds[52 + count].text_content()
            # Remove undesired elements from Site name
            if '\n' in site:
                site = site.replace('\n','')
            # Total Number of Fish Caught
            NumFish = (int(tds[58 + count].text_content())+int(tds[56 + count].text_content())+int(tds[55 + count].text_content()))
            # Number of Fish Per Angler (Total Fish Divided by Number of Anglers)
            NumAnglers = float(int(tds[54 + count].text_content()))
            data = {
                'Date' : tds[51 + count].text_content(),
                'Site' : site,
                'Number of Anglers' : int(tds[54 + count].text_content()),
                'Number of Chinook Salmon Caught' : int(tds[55 + count].text_content()),
                'Number of Coho Salmon Caught' : int(tds[56 + count].text_content()),
                'Number of Pink Salmon Caught' : int(tds[58 + count].text_content()),
                'Number of Fish Per Angler': NumFish/NumAnglers
            }
            # elements from same column and one row apart are 16 indexes apart    
            count += 16
            print data
            # Save data to Scraperwiki, thus making the data available for download
            scraperwiki.sqlite.save(unique_keys=['Site'], data=data)



# Function Calls
url_lst = extract_links(website, 20)
extract_data_from_reports(url_lst, 5)
            



#################################################################
### Description: This script returns catch reports from boat launches
### in Washington state along the Puget Sound and Peninsula.  There
### are two required inputs: a link to a wdfw catch report homepage
### and the desired number of records to be returned.


#################################################################
### Libraries
###

import scraperwiki
import lxml.html

#################################################################
### Script Follows
###

# Washington Department of Fish & Wildlife Website
website = "http://wdfw.wa.gov/fishing/creel/puget/2012/"

def extract_links(url, number_of_reports):
    '''
    Takes the link to a washington department fish and wildlife
    salmon catch homepage for a given year and the desired number
    of reports and returns the links to these individual report pages.
    '''
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    html_lst = []
    count = 0
    # links to individual catch reports are stored in the a tags of table rows
    for el in root.cssselect("tr a"):
        # the 103 index corresponds to the row containing data for the last week of
        # August, the end of the best time of year for salmon fishing in the Puget Sound.
        if count > 103 and count < (103+number_of_reports):
            html_catchreport =  el.attrib['href']
            # the extracted links are not the full link and need to be appended to the initial lin
            html2 = (url + html_catchreport)
            html_lst.append(html2)
        count += 1    
    return html_lst

def extract_data_from_reports(lst_of_url, number_of_records):
    '''
    Given a list of links to individual fishing reports from WDFW and the desired 
    number of reports return the following data: Date of Report, Site, Number of 
    Anglers, Number of Chinook caught, Number of Coho caught, Number of Pink Salmon 
    caught and lastly the Number of fish per angler.
    '''
    for url in lst_of_url:
        html = scraperwiki.scrape(url)
        root2 = lxml.html.fromstring(html)
        count = 0
        # Number of records to return from each link
        for i in range(number_of_records):
            tds = root2.cssselect("td")
            site = tds[52 + count].text_content()
            # Remove undesired elements from Site name
            if '\n' in site:
                site = site.replace('\n','')
            # Total Number of Fish Caught
            NumFish = (int(tds[58 + count].text_content())+int(tds[56 + count].text_content())+int(tds[55 + count].text_content()))
            # Number of Fish Per Angler (Total Fish Divided by Number of Anglers)
            NumAnglers = float(int(tds[54 + count].text_content()))
            data = {
                'Date' : tds[51 + count].text_content(),
                'Site' : site,
                'Number of Anglers' : int(tds[54 + count].text_content()),
                'Number of Chinook Salmon Caught' : int(tds[55 + count].text_content()),
                'Number of Coho Salmon Caught' : int(tds[56 + count].text_content()),
                'Number of Pink Salmon Caught' : int(tds[58 + count].text_content()),
                'Number of Fish Per Angler': NumFish/NumAnglers
            }
            # elements from same column and one row apart are 16 indexes apart    
            count += 16
            print data
            # Save data to Scraperwiki, thus making the data available for download
            scraperwiki.sqlite.save(unique_keys=['Site'], data=data)



# Function Calls
url_lst = extract_links(website, 20)
extract_data_from_reports(url_lst, 5)
            



