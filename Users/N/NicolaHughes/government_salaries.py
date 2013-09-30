import scraperwiki
import urllib
import urllib2
import StringIO
import json
import csv
import lxml.html
import urlparse

def links(url):
    lines = urllib.urlopen(url).readlines()
    header = []
    ok_headers = []
    ok_headers_indices = []
    clist = list(csv.reader(lines))
    #while clist[0][1] == "":
        #clist.pop(0)
    header = clist.pop(0)
    for i, h in enumerate(header):
        if h != '':
            ok_headers.append(h)
            ok_headers_indices.append(i)
    if ok_headers[-3] == 'Actual Pay Floor':
        ok_headers[-3] = 'Actual pay floor'
    if ok_headers[-2] == 'Actual Pay Ceiling':
        ok_headers[-2] = 'Actual pay ceiling'
    if ok_headers[0] == 'Post Unique Reference':
        del ok_headers[0]
    if ok_headers[-2] == 'Actual pay Floor':
        ok_headers[-2] = 'Actual pay floor'
    if ok_headers[-1] == 'Actual pay Ceiling':
        ok_headers[-1] = 'Actual pay ceiling'
    if ok_headers[0] == 'Post unique reference':
        del ok_headers[0]
    if ok_headers[0] == 'Unique Post ID':
        del ok_headers[0]
    if ok_headers[0] == 'Actual Name':
        del ok_headers[0]
    if ok_headers[0] == 'Full Name with Title':
        ok_headers[0] = 'Name'
        ok_headers[1] = 'Grade'
        ok_headers[2] = 'Job Title'
        ok_headers[3] = 'FTE'
        ok_headers[4] = 'Parent Department'
        ok_headers[5] = 'Organisation'
        ok_headers[6] = 'Unit'
        ok_headers[7] = 'Actual pay floor'
        ok_headers[8] = 'Actual pay ceiling'
    if ok_headers[1] == 'Actual Name':
        del ok_headers[1]
    if ok_headers[5] == 'Organsiation':
        ok_headers[5] = 'Organisation'
    if ok_headers[2] == 'Title':
        ok_headers[2] = 'Job Title'
    if ok_headers[4] == 'Department':
        ok_headers[4] = 'Parent Department'
    if ok_headers[7] == 'Salary Payband'or ok_headers[7] == 'Pay Band':
        ok_headers[7] = 'Actual pay floor'
        ok_headers[8] = 'Actual pay ceiling'
    if ok_headers[-1] == 'Notes':
        del ok_headers[-1]    
    if ok_headers[-1] == 'Comments':
        del ok_headers[-1]
    if ok_headers[6] == 'Business Area':
        ok_headers[6] = 'Unit'
    ok_headers = [x.strip() for x in ok_headers]
    #print ok_headers
    
    rownumber = 1

    for row in clist:
        if row and row[0]:
            # Only use this row if we have something in the first column.
            rownumber += 1
            filtered = [x[1] for x in enumerate(row) if x[0] in ok_headers_indices]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/AGOSeniorSalaries_0.csv':
                filtered = filtered[:7]+filtered[7].split(' - ')
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/BIS-senior-salaries.csv':
                del filtered[-1]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/CLGSeniorSalaries.csv':
                del filtered[-1]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/decc-senior-salaries_0.csv':
                del filtered[-1]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/GONetwork-Senior-Salaries.csv':
                del filtered[0:2]
                del filtered[-1]
            #if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/DfESeniorStaffPay_0.csv':
                #del filtered[-1]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/homeoffice-senior-salaries.csv':
                filtered = filtered[:7]+filtered[7].split('-')
                filtered = [x.strip() for x in filtered]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/tsolseniorstaffsalaries.csv':
                filtered = filtered[:7]+filtered[7].split(' - ')
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/health-senior-salaries.csv':
                filtered = filtered[0:2]+[""]+filtered[2:8]
            #print filtered
            if filtered[1] != "":                
                data = dict(zip(ok_headers, [x.decode('latin-1').encode('utf-8') for x in filtered]))                 
                data['Row_Number'] = rownumber
                data['URL'] = anyurl2
                try:
                    data['Actual pay floor'] = float(data['Actual pay floor'].replace(',','').replace('£',''))
                except ValueError:
                    data['Actual pay floor'] = ''
                try:
                    data['Actual pay ceiling'] = float(data['Actual pay ceiling'].replace(',','').replace('£',''))
                except ValueError:
                    data['Actual pay ceiling'] = ''
                except Exception, ex:
                    print ex
                    print data
                    print ok_headers
                    print filtered
                    print row
                    import sys
                    sys.exit()
                #print data
                scraperwiki.sqlite.save(unique_keys=['Row_Number', 'URL'], data=data)

#This is getting all the urls of the data entries in the cabinet office resource library which give the structure of each department#

for n in range(4):    
    url = "http://www.cabinetoffice.gov.uk/resource-library/type/434?page=%d" % n
    root = lxml.html.parse(url).getroot()
    if root == None:
        print "Root is unexpectedly None", url
    #print root
    for el in root.cssselect("div.view-content a"):           
        anyurl = el.attrib.get("href")
        #print anyurl       
        if "structure" in anyurl:            
            url2 = urlparse.urljoin(url,anyurl)
            #print url2
            
#This is getting the .csv downloads on staff salaries from the above urls#
            
            root = lxml.html.parse(url2).getroot()
            anchors = root.cssselect("div.downloadfile a")
            for el in anchors:
                anyurl2 = el.attrib.get("href")
                if (("Salaries" in anyurl2) and (".csv" in anyurl2)) or (("Pay" in anyurl2) and (".csv" in anyurl2)) or (("salaries" in anyurl2) and (".csv" in anyurl2)) or (("pay" in anyurl2) and (".csv" in anyurl2)):
                    #print anyurl2
                    links(anyurl2)

import scraperwiki
import urllib
import urllib2
import StringIO
import json
import csv
import lxml.html
import urlparse

def links(url):
    lines = urllib.urlopen(url).readlines()
    header = []
    ok_headers = []
    ok_headers_indices = []
    clist = list(csv.reader(lines))
    #while clist[0][1] == "":
        #clist.pop(0)
    header = clist.pop(0)
    for i, h in enumerate(header):
        if h != '':
            ok_headers.append(h)
            ok_headers_indices.append(i)
    if ok_headers[-3] == 'Actual Pay Floor':
        ok_headers[-3] = 'Actual pay floor'
    if ok_headers[-2] == 'Actual Pay Ceiling':
        ok_headers[-2] = 'Actual pay ceiling'
    if ok_headers[0] == 'Post Unique Reference':
        del ok_headers[0]
    if ok_headers[-2] == 'Actual pay Floor':
        ok_headers[-2] = 'Actual pay floor'
    if ok_headers[-1] == 'Actual pay Ceiling':
        ok_headers[-1] = 'Actual pay ceiling'
    if ok_headers[0] == 'Post unique reference':
        del ok_headers[0]
    if ok_headers[0] == 'Unique Post ID':
        del ok_headers[0]
    if ok_headers[0] == 'Actual Name':
        del ok_headers[0]
    if ok_headers[0] == 'Full Name with Title':
        ok_headers[0] = 'Name'
        ok_headers[1] = 'Grade'
        ok_headers[2] = 'Job Title'
        ok_headers[3] = 'FTE'
        ok_headers[4] = 'Parent Department'
        ok_headers[5] = 'Organisation'
        ok_headers[6] = 'Unit'
        ok_headers[7] = 'Actual pay floor'
        ok_headers[8] = 'Actual pay ceiling'
    if ok_headers[1] == 'Actual Name':
        del ok_headers[1]
    if ok_headers[5] == 'Organsiation':
        ok_headers[5] = 'Organisation'
    if ok_headers[2] == 'Title':
        ok_headers[2] = 'Job Title'
    if ok_headers[4] == 'Department':
        ok_headers[4] = 'Parent Department'
    if ok_headers[7] == 'Salary Payband'or ok_headers[7] == 'Pay Band':
        ok_headers[7] = 'Actual pay floor'
        ok_headers[8] = 'Actual pay ceiling'
    if ok_headers[-1] == 'Notes':
        del ok_headers[-1]    
    if ok_headers[-1] == 'Comments':
        del ok_headers[-1]
    if ok_headers[6] == 'Business Area':
        ok_headers[6] = 'Unit'
    ok_headers = [x.strip() for x in ok_headers]
    #print ok_headers
    
    rownumber = 1

    for row in clist:
        if row and row[0]:
            # Only use this row if we have something in the first column.
            rownumber += 1
            filtered = [x[1] for x in enumerate(row) if x[0] in ok_headers_indices]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/AGOSeniorSalaries_0.csv':
                filtered = filtered[:7]+filtered[7].split(' - ')
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/BIS-senior-salaries.csv':
                del filtered[-1]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/CLGSeniorSalaries.csv':
                del filtered[-1]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/decc-senior-salaries_0.csv':
                del filtered[-1]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/GONetwork-Senior-Salaries.csv':
                del filtered[0:2]
                del filtered[-1]
            #if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/DfESeniorStaffPay_0.csv':
                #del filtered[-1]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/homeoffice-senior-salaries.csv':
                filtered = filtered[:7]+filtered[7].split('-')
                filtered = [x.strip() for x in filtered]
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/tsolseniorstaffsalaries.csv':
                filtered = filtered[:7]+filtered[7].split(' - ')
            if anyurl2 == 'http://www.cabinetoffice.gov.uk/sites/default/files/resources/health-senior-salaries.csv':
                filtered = filtered[0:2]+[""]+filtered[2:8]
            #print filtered
            if filtered[1] != "":                
                data = dict(zip(ok_headers, [x.decode('latin-1').encode('utf-8') for x in filtered]))                 
                data['Row_Number'] = rownumber
                data['URL'] = anyurl2
                try:
                    data['Actual pay floor'] = float(data['Actual pay floor'].replace(',','').replace('£',''))
                except ValueError:
                    data['Actual pay floor'] = ''
                try:
                    data['Actual pay ceiling'] = float(data['Actual pay ceiling'].replace(',','').replace('£',''))
                except ValueError:
                    data['Actual pay ceiling'] = ''
                except Exception, ex:
                    print ex
                    print data
                    print ok_headers
                    print filtered
                    print row
                    import sys
                    sys.exit()
                #print data
                scraperwiki.sqlite.save(unique_keys=['Row_Number', 'URL'], data=data)

#This is getting all the urls of the data entries in the cabinet office resource library which give the structure of each department#

for n in range(4):    
    url = "http://www.cabinetoffice.gov.uk/resource-library/type/434?page=%d" % n
    root = lxml.html.parse(url).getroot()
    if root == None:
        print "Root is unexpectedly None", url
    #print root
    for el in root.cssselect("div.view-content a"):           
        anyurl = el.attrib.get("href")
        #print anyurl       
        if "structure" in anyurl:            
            url2 = urlparse.urljoin(url,anyurl)
            #print url2
            
#This is getting the .csv downloads on staff salaries from the above urls#
            
            root = lxml.html.parse(url2).getroot()
            anchors = root.cssselect("div.downloadfile a")
            for el in anchors:
                anyurl2 = el.attrib.get("href")
                if (("Salaries" in anyurl2) and (".csv" in anyurl2)) or (("Pay" in anyurl2) and (".csv" in anyurl2)) or (("salaries" in anyurl2) and (".csv" in anyurl2)) or (("pay" in anyurl2) and (".csv" in anyurl2)):
                    #print anyurl2
                    links(anyurl2)

