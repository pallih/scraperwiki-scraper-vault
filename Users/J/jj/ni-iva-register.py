# To collect data from the NI IVA register

import mechanize
import re
import scraperwiki
from BeautifulSoup import BeautifulSoup

br = mechanize.Browser()
br.open("http://www.business.detini.gov.uk/iva_register/IVASearch.aspx")
br.select_form(name="aspnetForm")
#br['ctl00$ContentPlaceHolder1$Surname']= "McMullan" # comment to search all
response = br.submit()

#scraperwiki.sqlite.save('data_columns', ['Surname', 'Forename', 'DOB', 'Address', 'Postcode', 'latlng'])

soup = BeautifulSoup(response)

tds = soup.find("table", { "id" : "ctl00_ContentPlaceHolder1_GridView1" } )
rows = tds.findAll("tr")

for row in rows:
    record = {}
    table_cells = row.findAll("td")
    if table_cells:
        surname =  re.sub("(\(.*)|( nee.*)", '', (re.sub("(\s[a|A]ka.*)|(\sformerly.*)", '', table_cells[0].text)))
        surname = re.sub("\s", '', surname)
        record['Surname'] = surname
        record['Forename'] = table_cells[1].text
        dob = re.sub('&nbsp;', "Unknown" , table_cells[2].text)
        record['DOB'] = dob
        address = table_cells[3].text
        postcode = re.findall("[A-Z|a-z][A-Z|a-z]\s*\d+\s*\d+\s*[A-Z|a-z]+", address)

        latlng = None
        if postcode:
            address = re.sub(postcode[0], '', address)
            postcode[0] = re.sub("\s", '', postcode[0])
            record['Postcode'] = postcode[0]
#comment out following 3
#            getlatlon(postcode[0])
            latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode[0]) # so slow
            record['latlng'] = latlng
        else:
            record['Postcode'] = "Unknown"
        address = re.sub(',\s*$', '', address) 
        record['Address'] = address
        scraperwiki.sqlite.save(unique_keys=["Address"], data=record)
