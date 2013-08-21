import scraperwiki
import requests
import lxml.html
import mechanize


linkList = []

#Function to get the names and links of the most wanted
def getLinks(url):
    html = requests.get(url).text
    br = mechanize.Browser()
    br.set_handle_robots(False)
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div.links a"):
        linkList.append(el.attrib['href'])

#Function to get info on criminals
def getInfo(url) : 
    html = requests.get(url).text
    br = mechanize.Browser()
    br.set_handle_robots(False)
    root = lxml.html.fromstring(html)
    infoList = []
    for datas in root.cssselect("table[class='table_detail_profil table_detail_profil_result_datasheet']")[2]:        
        for info in datas.cssselect("td[class='col2 strong']"):
            infoList.append(info.text_content())
    try: 
        surname = infoList[0]
    except IndexError:
        surname = ""
    try: 
        name = infoList[1]
    except IndexError:
        name = ""
    try: 
        sex = infoList[2]
    except IndexError:
        sex = ""
    try: 
        date = infoList[3]
    except IndexError:
        date = ""
    try: 
        charges = [charges.text_content() for charges in root.cssselect("p[class='charge']")]
    except IndexError:
        charges = ""
    try: 
        wanted= [wanted.text_content() for wanted in root.cssselect("span[class='nom_fugitif_wanted_small']")]
    except IndexError:
        wanted = ""
    
    data = {
        'Surname' : surname,
        'Name' : name,
        'Sex' : sex,
        'Date of Birth': date,
        'Nationality' : infoList[-1],
        'Charges' : charges,
        'Wanted by': wanted,
        'Link' : url,
            }
    scraperwiki.sqlite.save(unique_keys = ['Link'], data=data)

#Get the number of pages in the database
#source = 'http://www.interpol.int/Wanted-Persons'
#html = requests.get(source).text
#br = mechanize.Browser()
#br.set_handle_robots(False)
#root = lxml.html.fromstring(html)
#pages = root.cssselect("span[class='other']")
#pageList = [page.text_content() for page in pages]
#lastPage = int(pageList[-1])

#Loop through all the pages of the database to get the links
#(the 9 of the "nextpage" is due to have the links change to move to the next page)
#i = 0
#nextPage = 9
#getLinks(source)
#while i <= lastPage :
#    source2 = 'http://www.interpol.int/Wanted-Persons/(offset)/'+str(nextPage)
#    getLinks(source2)
#    nextPage = nextPage + 9
#    i = i + 1

#Loop through all single records to get info
#for link in linkList:
#    sourceCriminal = 'http://www.interpol.int'+link
#    getInfo(sourceCriminal)    
url = 'http://www.interpol.int/Wanted-Persons/(wanted_id)/2013-19960'
getInfo(url)