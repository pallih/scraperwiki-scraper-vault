import scraperwiki
import lxml.html

# Find openings, holdovers, and soon to be finished positions on mass board

#polareas = ['A%26F', 'EDU', 'ENV', 'OHS', 'C%26D', 'LAB', 'MISC', 'DPL', 'EPS', 'T%26C']
newpolareas = ['LAB', 'MISC', 'DPL', 'EPS', 'T%26C'] #In case it doesn't catch all
base = 'http://appointments.state.ma.us/Results.aspx?PolArea='

fields = {'A%26F': 'Administration and Finance', 'EDU': 'Education', 'ENV': 'Energy and Environmenal Affairs', 'OHS': 'Health and Human Services', 'C%26D': 'Housing and Economic Development', 'LAB': 'Labor and Workforce Development', 'MISC': 'Miscellanious', 'DPL': 'Professional Licensure', 'EPS': 'Public Safety', 'T%26C': 'Transportation and Public Works'} 

for i in newpolareas:
    pagename = base + i
    page = scraperwiki.scrape(pagename)
    pageroot = lxml.html.fromstring(page)
    for link in pageroot.cssselect('tr a'):
        doclink = link.attrib['href']
        docpagename = 'http://appointments.state.ma.us/' + doclink
        docpage = scraperwiki.scrape(docpagename) 
        docpageroot =  lxml.html.fromstring(docpage)
        for t in docpageroot.cssselect('span#ctl00_ContentPlaceHolder1_lblTitle'):
            title = t.text
        for row in docpageroot.cssselect('table#ctl00_ContentPlaceHolder1_gvwSeats tr'):
            for name in row.cssselect('td:nth-child(1)'):
                if name.text == 'VACANT':
                    status = 'Vacant'
                    pos = row.text_content()
                    pos = pos.replace('VACANT', '')
                    data = {'Area': fields[i], 'Board': title, 'Pos': pos, 'Status': 'Vacant'}
                    scraperwiki.sqlite.save(unique_keys = ['Pos'], data = data)
            
            
            import scraperwiki
import lxml.html

# Find openings, holdovers, and soon to be finished positions on mass board

#polareas = ['A%26F', 'EDU', 'ENV', 'OHS', 'C%26D', 'LAB', 'MISC', 'DPL', 'EPS', 'T%26C']
newpolareas = ['LAB', 'MISC', 'DPL', 'EPS', 'T%26C'] #In case it doesn't catch all
base = 'http://appointments.state.ma.us/Results.aspx?PolArea='

fields = {'A%26F': 'Administration and Finance', 'EDU': 'Education', 'ENV': 'Energy and Environmenal Affairs', 'OHS': 'Health and Human Services', 'C%26D': 'Housing and Economic Development', 'LAB': 'Labor and Workforce Development', 'MISC': 'Miscellanious', 'DPL': 'Professional Licensure', 'EPS': 'Public Safety', 'T%26C': 'Transportation and Public Works'} 

for i in newpolareas:
    pagename = base + i
    page = scraperwiki.scrape(pagename)
    pageroot = lxml.html.fromstring(page)
    for link in pageroot.cssselect('tr a'):
        doclink = link.attrib['href']
        docpagename = 'http://appointments.state.ma.us/' + doclink
        docpage = scraperwiki.scrape(docpagename) 
        docpageroot =  lxml.html.fromstring(docpage)
        for t in docpageroot.cssselect('span#ctl00_ContentPlaceHolder1_lblTitle'):
            title = t.text
        for row in docpageroot.cssselect('table#ctl00_ContentPlaceHolder1_gvwSeats tr'):
            for name in row.cssselect('td:nth-child(1)'):
                if name.text == 'VACANT':
                    status = 'Vacant'
                    pos = row.text_content()
                    pos = pos.replace('VACANT', '')
                    data = {'Area': fields[i], 'Board': title, 'Pos': pos, 'Status': 'Vacant'}
                    scraperwiki.sqlite.save(unique_keys = ['Pos'], data = data)
            
            
            