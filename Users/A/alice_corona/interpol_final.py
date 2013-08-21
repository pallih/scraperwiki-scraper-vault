import scraperwiki
import requests
import lxml.html
import mechanize

countryList = []
linkList = []


#FUNCTION TO GET A HREF OF CRIMINALS
def getLinks(url):
    html = requests.get(url).text
    br = mechanize.Browser()
    br.set_handle_robots(False)
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div.links a"):
        linkList.append(el.attrib['href'])

#FUNTION TO GET INFO ON CRIMINALS
def getInfo(url) : 
    html = requests.get(url).text
    br = mechanize.Browser()
    br.set_handle_robots(False)
    root = lxml.html.fromstring(html)
    infoList = []
#this can probably be done in a much more nicer way...but got sick of trying, as I had to wait hours of scraping each time to then get an error -.-
    try:
        for datas in root.cssselect("table[class='table_detail_profil table_detail_profil_result_datasheet']")[0]:        
            for info in datas.cssselect("td[class='col2 strong']"):
                infoList.append(info.text_content())
    except IndexError:
        a= ["","","",""]
        infoList.append(a)
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



#Get country codes to build urls
url = 'http://www.interpol.int/Wanted-Persons?lastname=&Forenames=&IPSGT_ICPO_Countries=102&free=&current_age_mini=0&current_age_maxi=100&IPSGT_Sex=&IPSGT_Eyes_Color=&IPSGT_Hair=&IPSGT_Interpol_Office=&wanted_search='
html = requests.get(url).text
br = mechanize.Browser()
br.set_handle_robots(False)
root = lxml.html.fromstring(html)
for optgroup in root.cssselect("select[name='IPSGT_ICPO_Countries']"):
    for option in optgroup.cssselect("option"):
            countryCode = option.get("value")
            countryList.append(countryCode)
countryList.pop(0)

#Loop through all countries in the database to get information
for country in countryList:
    if countryList.index(country) >= 97:
        source1 = url = 'http://www.interpol.int/Wanted-Persons?lastname=&Forenames=&IPSGT_ICPO_Countries='+country+'&free=&current_age_mini=0&current_age_maxi=100&IPSGT_Sex=&IPSGT_Eyes_Color=&IPSGT_Hair=&IPSGT_Interpol_Office=&wanted_search='

    #Get the number of pages in the database for this country
        html = requests.get(source1).text
        br = mechanize.Browser()
        br.set_handle_robots(False)
        root = lxml.html.fromstring(html)
        pages = root.cssselect("span[class='other']")
        pageList = [page.text_content() for page in pages]

    #Get the a href links of the most wanted for this country
        getLinks(source1)
        if len(pageList) != 0: 
            lastPage = int(pageList[-1])
            i = 0
            nextPage = 9
            while i <= lastPage :
                source2 = 'http://www.interpol.int/Wanted-Persons/(offset)/'+str(nextPage)+'?wanted_search=&IPSGT_ICPO_Countries='+country+'&current_age_mini=0&current_age_maxi=100'
                getLinks(source2)
                nextPage = nextPage + 9
                i = i + 1
#print linkList 
#Open the pages of the criminals and save the needed information
for link in linkList:
    sourceCriminal = 'http://www.interpol.int'+link
    getInfo(sourceCriminal)    
