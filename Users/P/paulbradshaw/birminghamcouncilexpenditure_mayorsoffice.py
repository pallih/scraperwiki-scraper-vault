import scraperwiki
import lxml.html
import csv
#more on csv library: https://scraperwiki.com/docs/python/python_csv_guide/


#page with links: 
url = 'http://www.birmingham.gov.uk/payment-data'
baseurl = 'http://www.birmingham.gov.uk'

def scrape_and_find_csv(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    #this selects all HTML containing link: <p class="fileicon"><a>
    csvs = root.cssselect('p.fileicon a')
    print csvs
    for link in csvs:
        #this prints the result of adding the base URL to the relative link grabbed
        fullurl = baseurl+link.attrib.get('href')
        print link.attrib.get('href')[-3:]
        if link.attrib.get('href')[-3:] == "csv":
            data = scraperwiki.scrape(baseurl+link.attrib.get('href'))
            reader = csv.DictReader(data.splitlines())
            for row in reader:
#                print row[' Invoice Amount '][0:]
#                row['missingletter'] = row[' Invoice Amount '][0]
#                row[' Invoice Amount_full'] = row[' Invoice Amount '].decode("latin-1")
#AttributeError: 'NoneType' object has no attribute 'decode'
                if row['Cost Cente'] == 'RBL23':
                    if row['Invoice Ref'] is not None:
                        row['Invoice Ref'] = row['Invoice Ref'].decode("latin-1")
                    row[' Invoice Amount '] = row[' Invoice Amount '][2:]
                    row['URL'] = fullurl
                    print row
                    if row['Doc Number'] is not None:
                        scraperwiki.sqlite.save(['Doc Number', 'URL'], row)
#                    else: 
 #                       row['Doc Number'] = "NO ENTRY"
  #                      scraperwiki.sqlite.save(['Doc Number', 'URL'], row)

#STARTS WORKING HERE!
scrape_and_find_csv(url)

#Have asked for ucsv library to be incorporated: http://stackoverflow.com/questions/1846135/python-csv-library-with-unicode-utf-8-support-that-just-works
import scraperwiki
import lxml.html
import csv
#more on csv library: https://scraperwiki.com/docs/python/python_csv_guide/


#page with links: 
url = 'http://www.birmingham.gov.uk/payment-data'
baseurl = 'http://www.birmingham.gov.uk'

def scrape_and_find_csv(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    #this selects all HTML containing link: <p class="fileicon"><a>
    csvs = root.cssselect('p.fileicon a')
    print csvs
    for link in csvs:
        #this prints the result of adding the base URL to the relative link grabbed
        fullurl = baseurl+link.attrib.get('href')
        print link.attrib.get('href')[-3:]
        if link.attrib.get('href')[-3:] == "csv":
            data = scraperwiki.scrape(baseurl+link.attrib.get('href'))
            reader = csv.DictReader(data.splitlines())
            for row in reader:
#                print row[' Invoice Amount '][0:]
#                row['missingletter'] = row[' Invoice Amount '][0]
#                row[' Invoice Amount_full'] = row[' Invoice Amount '].decode("latin-1")
#AttributeError: 'NoneType' object has no attribute 'decode'
                if row['Cost Cente'] == 'RBL23':
                    if row['Invoice Ref'] is not None:
                        row['Invoice Ref'] = row['Invoice Ref'].decode("latin-1")
                    row[' Invoice Amount '] = row[' Invoice Amount '][2:]
                    row['URL'] = fullurl
                    print row
                    if row['Doc Number'] is not None:
                        scraperwiki.sqlite.save(['Doc Number', 'URL'], row)
#                    else: 
 #                       row['Doc Number'] = "NO ENTRY"
  #                      scraperwiki.sqlite.save(['Doc Number', 'URL'], row)

#STARTS WORKING HERE!
scrape_and_find_csv(url)

#Have asked for ucsv library to be incorporated: http://stackoverflow.com/questions/1846135/python-csv-library-with-unicode-utf-8-support-that-just-works
import scraperwiki
import lxml.html
import csv
#more on csv library: https://scraperwiki.com/docs/python/python_csv_guide/


#page with links: 
url = 'http://www.birmingham.gov.uk/payment-data'
baseurl = 'http://www.birmingham.gov.uk'

def scrape_and_find_csv(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    #this selects all HTML containing link: <p class="fileicon"><a>
    csvs = root.cssselect('p.fileicon a')
    print csvs
    for link in csvs:
        #this prints the result of adding the base URL to the relative link grabbed
        fullurl = baseurl+link.attrib.get('href')
        print link.attrib.get('href')[-3:]
        if link.attrib.get('href')[-3:] == "csv":
            data = scraperwiki.scrape(baseurl+link.attrib.get('href'))
            reader = csv.DictReader(data.splitlines())
            for row in reader:
#                print row[' Invoice Amount '][0:]
#                row['missingletter'] = row[' Invoice Amount '][0]
#                row[' Invoice Amount_full'] = row[' Invoice Amount '].decode("latin-1")
#AttributeError: 'NoneType' object has no attribute 'decode'
                if row['Cost Cente'] == 'RBL23':
                    if row['Invoice Ref'] is not None:
                        row['Invoice Ref'] = row['Invoice Ref'].decode("latin-1")
                    row[' Invoice Amount '] = row[' Invoice Amount '][2:]
                    row['URL'] = fullurl
                    print row
                    if row['Doc Number'] is not None:
                        scraperwiki.sqlite.save(['Doc Number', 'URL'], row)
#                    else: 
 #                       row['Doc Number'] = "NO ENTRY"
  #                      scraperwiki.sqlite.save(['Doc Number', 'URL'], row)

#STARTS WORKING HERE!
scrape_and_find_csv(url)

#Have asked for ucsv library to be incorporated: http://stackoverflow.com/questions/1846135/python-csv-library-with-unicode-utf-8-support-that-just-works
