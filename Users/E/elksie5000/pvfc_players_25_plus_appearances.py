import scraperwiki
import lxml.html
import requests
from datetime import datetime
import re

base_url = "http://en.wikipedia.org/wiki/List_of_Port_Vale_F.C._players"
wiki_url = "http://en.wikipedia.org"
table_xpath = '//*[@id="mw-content-text"]/table[1]'
column_header = '//*[@id="mw-content-text"]/table[1]/thead/tr/th[1]'
row_xpath = '//*[@id="mw-content-text"]/table[1]//tr'
player_xpath ='/td[1]/span/span/a'

alternate_date = re.compile("\d\d [A-Za-z]* \d\d\d\d")


def scrape_player(scrape_url):
    global date_birth_object
    global place_of_birth
    f = requests.get(scrape_url)
    html = f.text
    root = lxml.html.fromstring(html)
    player_data_headers = root.cssselect('table.infobox.vcard tr')
    for el in player_data_headers:
        if "Date of birth" in lxml.html.tostring(el):
            date_of_birth = el.cssselect("td")[0].text_content()
            date_of_birth = date_of_birth.replace("[1]", "")
            date_of_birth = date_of_birth.replace("[2]", "")
            date_of_birth = date_of_birth.strip(" ")
            
            if "c." in date_of_birth:
                date_of_birth = date_of_birth.split("c.")
                print date_of_birth[1]
                date_of_birth = date_of_birth[1].strip()
                print date_of_birth
                date_birth_object = datetime.strptime(date_of_birth, '%Y')
            elif "Q1" in date_of_birth:
                date_of_birth = date_of_birth.split("Q1 ")
                print date_of_birth[1]
                date_birth_object = datetime.strptime(date_of_birth[1], '%Y')
            elif " or " in date_of_birth:
                date_of_birth = date_of_birth.split(" or ")
                print date_of_birth[1]
                date_birth_object = datetime.strptime(date_of_birth[0], '%Y')

            elif "March qtr, " in date_of_birth:
                date_of_birth = date_of_birth.split("March qtr, ")
                print date_of_birth[1]
                date_birth_object = datetime.strptime(date_of_birth[1], '%Y')
            elif "unknown" in date_of_birth:
                    data_birth_object = "NA"
            elif alternate_date.match(date_of_birth) !=None:
                date_birth_object = datetime.strptime(date_of_birth, '%d %B %Y')
            elif ")" not in date_of_birth:
                if date_of_birth.isdigit():
                    date_birth_object = datetime.strptime(date_of_birth, '%Y')
                else:
                    date_birth_object = datetime.strptime(date_of_birth, '%B %Y')
            
            else:  
                date_of_birth = date_of_birth.split(")")
                date_of_birth = date_of_birth[0].replace("(","")
                date_birth_object = datetime.strptime(date_of_birth, '%Y-%m-%d')
                print date_birth_object
        if "Place of birth" in lxml.html.tostring(el):
            place_of_birth = el.cssselect("td")[0].text_content()
            place_of_birth = place_of_birth.replace("[1]", "")
            place_of_birth = place_of_birth.replace("[2]", "")
    
    print date_birth_object, place_of_birth
    return date_birth_object, place_of_birth



f = requests.get(base_url)

html = f.text
root = lxml.html.fromstring(html)

rows = root.xpath(row_xpath)
print len(rows)
for row in rows[1:]:
    record = {}
    print lxml.html.tostring(row)
    player_nm = row.cssselect("span.fn")
    attributes = row.cssselect('td')
    
    record['player_name'] = player_nm[0].text_content()
    record['position']= attributes[2].text    
    record['time_with_vale'] = attributes[3].text
    record['appearances'] = attributes[4].text
    record['goals'] = attributes[5].text
    try:
        player_nm_tst = row.cssselect("span.fn a")
        record['url'] = wiki_url + player_nm_tst[0].attrib['href']
        print record['url']
    except:
        record['url'] = "NA"
        
    if record['url'] != "NA":
        record['birthdate'], record['birthplace'] = scrape_player(record['url'])
    else:
        record['birthdate'] = "NA"
        record['birthplace'] = "NA"
    print record
    scraperwiki.sqlite.save(unique_keys=['player_name'], data=record)

