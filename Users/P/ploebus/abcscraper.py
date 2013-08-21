# Blank Python
import urllib
import scraperwiki
import lxml.html
import re

params=urllib.urlencode({'q_CityLOV':'OAKLAND','q_LTLOV':'01','RPTYPE':'p_OffSale','SUBMIT1':'Continue'})
params=params.encode()
#print params
url="http://www.abc.ca.gov/datport/AHCityRep.asp"
html=urllib.urlopen(url,params).read()
#html=scraperwiki.scrape(url,params)


def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
root = lxml.html.fromstring(html) # turn our HTML into an lxml object

rows = root.cssselect("table tr.report_column")  # selects all <tr> blocks within <table class="data">
record = {}
for row in rows:
    #print row,'------------'
    # Set up our data record - we'll need it later
    
    table_cells = row.cssselect("td")
       
    
    if table_cells: 
        print dir('table_cells[6]')
        #record['Id'] = table_cells[0].text
        #record['License_Number'] = table_cells[1].text
        #record['Status'] = table_cells[2].text
        #record['IssueDate'] = table_cells[4].text
        #record['ExpData'] = table_cells[5].text
        #record['Place'] = table_cells[6].innertext
        #record['Owner'] = table_cells[7].text
        #record['MailAddress'] = table_cells[8].text
        #record['Geocode'] = table_cells[9].text
        #scraperwiki.sqlite.save(['Id'],record)
    
    # Print out the data we've gathered
        print table_cells[6].text_content()
    
    # Finally, save the record to the datastore - 'Artist' is our unique key

