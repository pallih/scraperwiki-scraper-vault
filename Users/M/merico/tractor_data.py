import scraperwiki
import urllib
import urllib2
import re
import unicodedata
from bs4 import BeautifulSoup


scraperwiki.sqlite.execute("drop table if exists Models")
scraperwiki.sqlite.commit()

#Request webpage
url = 'http://www.tractordata.com/farm-tractors/index.html'
values = {'name' : 'Michael Foord',
          'location' : 'Northampton',
          'language' : 'Python' }

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)

#Parse HTML
#Find Brands
key, datakey = 0, 0
soup = BeautifulSoup(response)
table = soup.find(class_="tdMenu1")
for row in table.findChildren("tr"):
    #Find Models for each brand
    tds = row.findChildren("td")
    brand = tds[0].string
    if len(tds) == 4:
        try:
            url = tds[0].a["href"]
            print(url)
            soup = BeautifulSoup(urllib2.urlopen(url), "html5lib")
            subtable = soup(class_="tdmenu1")
            links = subtable[0]("a")
            for a in links:
                #Find Specifications for each model
                model = a.text
                url = a["href"]
                soup = BeautifulSoup(urllib2.urlopen(url), "html5lib")
                allData = soup("td","tdat")
                #Save Model
                data = {
                    'key' : key,
                    'brand' : unicode(brand),
                    'model' : model,
                    'link' : url
                }
                key = key + 1
                for d in allData:
                    field = ""
                    try:
                        field = d.previous_sibling
                        field = field.text.replace(":","")
#MISSING: Get header info, handle data without field and data from the other tabbed sides.
                        #header = data.parent.find_previous_sibling("td","thdr")
                        #header = header.text.replace(":","")
                        #print(header)
                        #print(field, "=", d)
                    except Exception, e:
                        field = 'NA'+ unicode(datakey) ##Data with no field description could be gathered here
                        datakey = datakey + 1
                    field = unicodedata.normalize('NFKD', field).encode('ascii','ignore')
                    field = re.sub('[\W_]','',field) ##Strip non-alphanumeric charachters
                    if field=="":
                        field='NA'+ unicode(datakey)
                    data[field] = d.text ##Append the data to the dictionary using the "field" as key.
                    datakey = 0


##                headerCells = soup(class_="thdr")
##                tr = headerCells[0].parent
##                #print(tr.prettify)
##
##                for hc in headerCells:
##                    headerText = hc.h2.text
##
##                    #Stripping colon add the end if there is any
##                    if headerText[len(headerText)-1] == ':':
##                        headerText = headerText[0:len(headerText)-1]
##
##                    #This command gets the header text of the page
##                    #needle = soup.select("td.tdData3 h1")[0].text
##
##                    #Stripping model and brand from the headers
##                    #FIX: Get manufacturer field and strip this aswell
##                    headerText = headerText.replace(model,"")
##                    headerText = headerText.replace(brand,"")
##                    headerText = headerText.strip()
##                    print(headerText)
                scraperwiki.sqlite.save(unique_keys=['key'], data=data, table_name="Models")
        except IndexError:
            print("No models for this brand - proceeding...")

        #print(tds[0].string, tds[0].a['href'])