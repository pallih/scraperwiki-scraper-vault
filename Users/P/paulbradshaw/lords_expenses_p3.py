import scraperwiki
import requests
import openpyxl
import tempfile
import time
import pprint

BASEURL = 'http://www.parliament.uk/'
URL = 'http://www.parliament.uk/mps-lords-and-offices/members-allowances/house-of-lords/holallowances/hol-expenses04/201112/'
#set a variable for the spreadsheet location
XLS = 'http://www.parliament.uk/documents/lords-finance-office/2012-13/allowances-expenses-2012-13-month-10-january-2013.xlsx'

def getworkbook(url):
    # Loads an xlsx file from the internet
    raw = requests.get(url, verify=False).content
    f = tempfile.NamedTemporaryFile('wb')
    f.write(raw)
    f.seek(0)
    wb = openpyxl.load_workbook(f.name)
    f.close()
    return wb

def getdata(wb, sheet):
    #Turn a sheet on a workbook into an array
    data = wb.get_sheet_by_name(sheet)
    return [[unicode(cell.value).strip() for cell in row] for row in data.rows]

def import_data(linkurl):
    wb = getworkbook(linkurl)
    sheet_names = wb.get_sheet_names() 
    if not sheet_names:
        return
    # assume there's only 1 sheet, and get first one
    rows = getdata(wb, sheet_names[0])
    pprint.pprint(rows)

    expenses = {}
    headings = []
    record = {}
    for num in range(0,18):
#This grabs the headings in row 6 - but the second spreadsheet has these on row 7, breaking the scraper, so the elif line grabs those
        if rows[5][0] == "Name":
            print "rows[5][num]", rows[5][num]
            #various slashes, brackets and full stops caused problems as keys, so this line replaces them all
            cleanedheading = rows[5][num].replace("/","_").replace("No.","Number").replace("(","_").replace(")","_").replace("&","and")
            print "cleaned heading:", cleanedheading 
            headings.append(cleanedheading)
            print "headings:", headings
        elif rows[6][0] == "Name":
            print "rows[6][num]", rows[6][num]
            #various slashes, brackets and full stops caused problems as keys, so this line replaces them all
            cleanedheading = rows[6][num].replace("/","_").replace("No.","Number").replace("(","_").replace(")","_").replace("&","and")
            print "cleaned heading:", cleanedheading 
            headings.append(cleanedheading)
            print "headings:", headings
        else:
            print "NEITHER ROW?", linkurl
        
    for i in range(7,805):
        print rows[i][0]
        expenses['linkurl'] = linkurl
        for num in range(0,18):
            expenses[headings[num]] = rows[i][num]
        #this caused problems because the heading 'Name' has a capital 'n' which I overlooked
        scraperwiki.sqlite.save(['Name', 'linkurl'], expenses, 'expenses')
import scraperwiki
import lxml.html

def grabexcellinks(URL):
    #Use Scraperwiki's scrape function on 'URL', put results in new variable 'html'
    html = scraperwiki.scrape(URL)
    #and show it us
    print html
    #Use lxml.html's fromstring function on 'html', put results in new variable 'root'
    root = lxml.html.fromstring(html)
    #use cssselect method on 'root' to grab all <a> tags within a <li> tag - and put in a new list variable 'links'
    links = root.cssselect('div.rte li a')
    #for each item in that list variable, from the second to the 11th [1:10], put it in the variable 'link'
#PROBLEM with first XLSX - March, so this starts from the 4th link
    for link in links[1:4]:
        #and print the text_content of that (after the string "link text:")
        print "link text:", link.text_content()
        #use the attrib.get method on 'link' to grab the href= attribute of the HTML, and put in new 'linkurl' variable
        linkurl = link.attrib.get('href')
        #print it
        print "link type:", linkurl[-4:]
        #run the function scrapesheets, using that variable as the parameter
        if linkurl[-3:] == "xls":
            print "SCRAPE IT!"
            import_data('http://www.parliament.uk/'+linkurl)

grabexcellinks('http://www.parliament.uk/mps-lords-and-offices/members-allowances/house-of-lords/holallowances/hol-expenses04/201011/')

import scraperwiki
import requests
import openpyxl
import tempfile
import time
import pprint

BASEURL = 'http://www.parliament.uk/'
URL = 'http://www.parliament.uk/mps-lords-and-offices/members-allowances/house-of-lords/holallowances/hol-expenses04/201112/'
#set a variable for the spreadsheet location
XLS = 'http://www.parliament.uk/documents/lords-finance-office/2012-13/allowances-expenses-2012-13-month-10-january-2013.xlsx'

def getworkbook(url):
    # Loads an xlsx file from the internet
    raw = requests.get(url, verify=False).content
    f = tempfile.NamedTemporaryFile('wb')
    f.write(raw)
    f.seek(0)
    wb = openpyxl.load_workbook(f.name)
    f.close()
    return wb

def getdata(wb, sheet):
    #Turn a sheet on a workbook into an array
    data = wb.get_sheet_by_name(sheet)
    return [[unicode(cell.value).strip() for cell in row] for row in data.rows]

def import_data(linkurl):
    wb = getworkbook(linkurl)
    sheet_names = wb.get_sheet_names() 
    if not sheet_names:
        return
    # assume there's only 1 sheet, and get first one
    rows = getdata(wb, sheet_names[0])
    pprint.pprint(rows)

    expenses = {}
    headings = []
    record = {}
    for num in range(0,18):
#This grabs the headings in row 6 - but the second spreadsheet has these on row 7, breaking the scraper, so the elif line grabs those
        if rows[5][0] == "Name":
            print "rows[5][num]", rows[5][num]
            #various slashes, brackets and full stops caused problems as keys, so this line replaces them all
            cleanedheading = rows[5][num].replace("/","_").replace("No.","Number").replace("(","_").replace(")","_").replace("&","and")
            print "cleaned heading:", cleanedheading 
            headings.append(cleanedheading)
            print "headings:", headings
        elif rows[6][0] == "Name":
            print "rows[6][num]", rows[6][num]
            #various slashes, brackets and full stops caused problems as keys, so this line replaces them all
            cleanedheading = rows[6][num].replace("/","_").replace("No.","Number").replace("(","_").replace(")","_").replace("&","and")
            print "cleaned heading:", cleanedheading 
            headings.append(cleanedheading)
            print "headings:", headings
        else:
            print "NEITHER ROW?", linkurl
        
    for i in range(7,805):
        print rows[i][0]
        expenses['linkurl'] = linkurl
        for num in range(0,18):
            expenses[headings[num]] = rows[i][num]
        #this caused problems because the heading 'Name' has a capital 'n' which I overlooked
        scraperwiki.sqlite.save(['Name', 'linkurl'], expenses, 'expenses')
import scraperwiki
import lxml.html

def grabexcellinks(URL):
    #Use Scraperwiki's scrape function on 'URL', put results in new variable 'html'
    html = scraperwiki.scrape(URL)
    #and show it us
    print html
    #Use lxml.html's fromstring function on 'html', put results in new variable 'root'
    root = lxml.html.fromstring(html)
    #use cssselect method on 'root' to grab all <a> tags within a <li> tag - and put in a new list variable 'links'
    links = root.cssselect('div.rte li a')
    #for each item in that list variable, from the second to the 11th [1:10], put it in the variable 'link'
#PROBLEM with first XLSX - March, so this starts from the 4th link
    for link in links[1:4]:
        #and print the text_content of that (after the string "link text:")
        print "link text:", link.text_content()
        #use the attrib.get method on 'link' to grab the href= attribute of the HTML, and put in new 'linkurl' variable
        linkurl = link.attrib.get('href')
        #print it
        print "link type:", linkurl[-4:]
        #run the function scrapesheets, using that variable as the parameter
        if linkurl[-3:] == "xls":
            print "SCRAPE IT!"
            import_data('http://www.parliament.uk/'+linkurl)

grabexcellinks('http://www.parliament.uk/mps-lords-and-offices/members-allowances/house-of-lords/holallowances/hol-expenses04/201011/')

