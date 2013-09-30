import scraperwiki
import dateutil.parser
import requests
import sys
from BeautifulSoup import BeautifulSoup


def create_tables():              # This method creates the tables needed with their proper schemas.
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    #scraperwiki.sqlite.execute("drop table swvariables")
    scraperwiki.sqlite.execute("create table swdata('List Price' str, 'Amazon Price' str, 'Star Rating' date, '5-star Reviews' date, '4-star Reviews' str, '3-star Reviews' str, '2-star Reviews' str, '1-star Reviews' str, 'Total Reviews' str, 'Screen Size' str, 'Resolution' str, 'Brand' str, 'Model Number' str, 'Technology' str, 'Sales Rank' str, 'Date Added' datetime, 'Link' str)")
    #scraperwiki.sqlite.execute("create table swvariables('name' str, 'value_blob' date)")
    scraperwiki.sqlite.commit()

def clean(text):                  # This method removes the space code from strings
    if text.endswith("&nbsp;"):
        text = text[:-6]
    return text.strip('\t\n\r')

def get_data(link, list_price):
    headers_dict = {'user-agent': 'Mozilla/5.0'}
    html_link = requests.get(link, headers=headers_dict)
    root_link = BeautifulSoup(html_link.text)                                      # Parse the html into something BeautifulSoup can read

    record = {}
    if "None" in list_price:
        try:
            record['List Price'] = root_link.find('span',{"id" : "listPriceValue"}).text
        except:
            record['List Price'] = "None"                                              # LIST PRICE
    else: record['List Price'] = list_price

    try:
        record['Amazon Price'] = root_link.find('b',{"class" : "priceLarge"}).text # AMAZON PRICE
    except:
        record['Amazon Price'] = "None"

    record['Star Rating'] = root_link.find('div',{"class" : "gry txtnormal acrRating"}).text[:3]   # STAR RATING
    star = root_link.find('div',{"class" : "fl histoRowfive clearboth"})
    record['5-star Reviews'] = star.find('div',{"class" : "histoCount fl gl10 ltgry txtnormal"}).text
    star = root_link.find('div',{"class" : "fl histoRowfour clearboth"})
    record['4-star Reviews'] = star.find('div',{"class" : "histoCount fl gl10 ltgry txtnormal"}).text
    star = root_link.find('div',{"class" : "fl histoRowthree clearboth"})
    record['3-star Reviews'] = star.find('div',{"class" : "histoCount fl gl10 ltgry txtnormal"}).text
    star = root_link.find('div',{"class" : "fl histoRowtwo clearboth"})
    record['2-star Reviews'] = star.find('div',{"class" : "histoCount fl gl10 ltgry txtnormal"}).text
    star = root_link.find('div',{"class" : "fl histoRowone clearboth"})
    record['1-star Reviews'] = star.find('div',{"class" : "histoCount fl gl10 ltgry txtnormal"}).text
    record['Total Reviews'] = root_link.find('a',{"class" : "noTextDecoration"}).text              # TOTAL REVIEWS
    
    if "inch" or "Inch" in root_link.find('span',{"id": "btAsinTitle"}).text:
        title = root_link.find('span',{"id": "btAsinTitle"}).text.lower()
        record['Screen Size'] = title[title.find("-inch")-2:title.find("-inch")]
    else: record['Screen Size'] = "None"
    


    record['Link'] = link
    scraperwiki.sqlite.save(unique_keys=['Total Reviews'], data=record)# Save all data









create_tables()  
print "Scraping HTML from website..."                                           

# Attempts to connect to the website
try:
    headers_dict = {'user-agent': 'Mozilla/5.0'}
    html = requests.get('http://www.amazon.com/s/ref=sr_nr_p_n_size_browse-bin_7?rh=n%3A172282%2Ck%3Atelevision%2Cn%3A%21493964%2Cn%3A1266092011%2Cp_n_condition-type%3A2224371011%2Cn%3A172659%2Cp_n_size_browse-bin%3A1232881011%7C3578041011%7C1232882011%7C3578042011%7C1232883011&bbn=172659&keywords=television&ie=UTF8&qid=1351823919&rnid=1232878011', headers=headers_dict)
except:
    print "***ERROR: Connection to website failed. Exiting program.***"
    sys.exit(1) 
#html = scraperwiki.scrape('http://mbec.phila.gov/procurement/') # Scrape the html from the website
root = BeautifulSoup(html.text)                                      # Parse the html into something BeautifulSoup can read
print root

print "This is the link to use to go to different pages: http://www.amazon.com/s/ref=sr_pg_50?rh=n%3A172282%2Ck%3Atelevision%2Cn%3A%21493964%2Cn%3A1266092011%2Cp_n_condition-type%3A2224371011%2Cn%3A172659%2Cp_n_size_browse-bin%3A1232881011%7C3578041011%7C1232882011%7C3578042011%7C1232883011&page=50&bbn=172659&keywords=television&ie=UTF8&qid=1351825075"
print "Getting data..."

page = 1
count = root.find('div',{"class" : "srSprite spr_header hdr"})
count = count.find('h2',{"class" : "resultCount"}).text[12:14]
print count
print "On page 1..."
for i in range(0, 988):
    
    if i+1 > count:
        page += 1
        print "On page " + str(page) + "..."
        html = requests.get( ('http://www.amazon.com/s/ref=sr_pg_'+ str(page) + '?rh=n%3A172282%2Ck%3Atelevision%2Cn%3A%21493964%2Cn%3A1266092011%2Cp_n_condition-type%3A2224371011%2Cn%3A172659%2Cp_n_size_browse-bin%3A1232881011%7C3578041011%7C1232882011%7C3578042011%7C1232883011&page=' + str(page) + '&bbn=172659&keywords=television&ie=UTF8&qid=1351825075' ), headers=headers_dict)
        root = BeautifulSoup(html.text)                                      # Parse the html into something BeautifulSoup can read
        count = root.find('div',{"class" : "srSprite spr_header hdr"})
        count = count.find('h2',{"class" : "resultCount"}).text[12:14]
    link_div = root.find('div',{"id" : ("result_" + str(i))})
    print "Link " + str(i)
    link = link_div.find('a',href=True)['href'] 
    try:
        list_price = link_div.find('del',{"class" : "grey"}).text
    except:
        list_price = "None"

    get_data(link, list_price)


import scraperwiki
import dateutil.parser
import requests
import sys
from BeautifulSoup import BeautifulSoup


def create_tables():              # This method creates the tables needed with their proper schemas.
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    #scraperwiki.sqlite.execute("drop table swvariables")
    scraperwiki.sqlite.execute("create table swdata('List Price' str, 'Amazon Price' str, 'Star Rating' date, '5-star Reviews' date, '4-star Reviews' str, '3-star Reviews' str, '2-star Reviews' str, '1-star Reviews' str, 'Total Reviews' str, 'Screen Size' str, 'Resolution' str, 'Brand' str, 'Model Number' str, 'Technology' str, 'Sales Rank' str, 'Date Added' datetime, 'Link' str)")
    #scraperwiki.sqlite.execute("create table swvariables('name' str, 'value_blob' date)")
    scraperwiki.sqlite.commit()

def clean(text):                  # This method removes the space code from strings
    if text.endswith("&nbsp;"):
        text = text[:-6]
    return text.strip('\t\n\r')

def get_data(link, list_price):
    headers_dict = {'user-agent': 'Mozilla/5.0'}
    html_link = requests.get(link, headers=headers_dict)
    root_link = BeautifulSoup(html_link.text)                                      # Parse the html into something BeautifulSoup can read

    record = {}
    if "None" in list_price:
        try:
            record['List Price'] = root_link.find('span',{"id" : "listPriceValue"}).text
        except:
            record['List Price'] = "None"                                              # LIST PRICE
    else: record['List Price'] = list_price

    try:
        record['Amazon Price'] = root_link.find('b',{"class" : "priceLarge"}).text # AMAZON PRICE
    except:
        record['Amazon Price'] = "None"

    record['Star Rating'] = root_link.find('div',{"class" : "gry txtnormal acrRating"}).text[:3]   # STAR RATING
    star = root_link.find('div',{"class" : "fl histoRowfive clearboth"})
    record['5-star Reviews'] = star.find('div',{"class" : "histoCount fl gl10 ltgry txtnormal"}).text
    star = root_link.find('div',{"class" : "fl histoRowfour clearboth"})
    record['4-star Reviews'] = star.find('div',{"class" : "histoCount fl gl10 ltgry txtnormal"}).text
    star = root_link.find('div',{"class" : "fl histoRowthree clearboth"})
    record['3-star Reviews'] = star.find('div',{"class" : "histoCount fl gl10 ltgry txtnormal"}).text
    star = root_link.find('div',{"class" : "fl histoRowtwo clearboth"})
    record['2-star Reviews'] = star.find('div',{"class" : "histoCount fl gl10 ltgry txtnormal"}).text
    star = root_link.find('div',{"class" : "fl histoRowone clearboth"})
    record['1-star Reviews'] = star.find('div',{"class" : "histoCount fl gl10 ltgry txtnormal"}).text
    record['Total Reviews'] = root_link.find('a',{"class" : "noTextDecoration"}).text              # TOTAL REVIEWS
    
    if "inch" or "Inch" in root_link.find('span',{"id": "btAsinTitle"}).text:
        title = root_link.find('span',{"id": "btAsinTitle"}).text.lower()
        record['Screen Size'] = title[title.find("-inch")-2:title.find("-inch")]
    else: record['Screen Size'] = "None"
    


    record['Link'] = link
    scraperwiki.sqlite.save(unique_keys=['Total Reviews'], data=record)# Save all data









create_tables()  
print "Scraping HTML from website..."                                           

# Attempts to connect to the website
try:
    headers_dict = {'user-agent': 'Mozilla/5.0'}
    html = requests.get('http://www.amazon.com/s/ref=sr_nr_p_n_size_browse-bin_7?rh=n%3A172282%2Ck%3Atelevision%2Cn%3A%21493964%2Cn%3A1266092011%2Cp_n_condition-type%3A2224371011%2Cn%3A172659%2Cp_n_size_browse-bin%3A1232881011%7C3578041011%7C1232882011%7C3578042011%7C1232883011&bbn=172659&keywords=television&ie=UTF8&qid=1351823919&rnid=1232878011', headers=headers_dict)
except:
    print "***ERROR: Connection to website failed. Exiting program.***"
    sys.exit(1) 
#html = scraperwiki.scrape('http://mbec.phila.gov/procurement/') # Scrape the html from the website
root = BeautifulSoup(html.text)                                      # Parse the html into something BeautifulSoup can read
print root

print "This is the link to use to go to different pages: http://www.amazon.com/s/ref=sr_pg_50?rh=n%3A172282%2Ck%3Atelevision%2Cn%3A%21493964%2Cn%3A1266092011%2Cp_n_condition-type%3A2224371011%2Cn%3A172659%2Cp_n_size_browse-bin%3A1232881011%7C3578041011%7C1232882011%7C3578042011%7C1232883011&page=50&bbn=172659&keywords=television&ie=UTF8&qid=1351825075"
print "Getting data..."

page = 1
count = root.find('div',{"class" : "srSprite spr_header hdr"})
count = count.find('h2',{"class" : "resultCount"}).text[12:14]
print count
print "On page 1..."
for i in range(0, 988):
    
    if i+1 > count:
        page += 1
        print "On page " + str(page) + "..."
        html = requests.get( ('http://www.amazon.com/s/ref=sr_pg_'+ str(page) + '?rh=n%3A172282%2Ck%3Atelevision%2Cn%3A%21493964%2Cn%3A1266092011%2Cp_n_condition-type%3A2224371011%2Cn%3A172659%2Cp_n_size_browse-bin%3A1232881011%7C3578041011%7C1232882011%7C3578042011%7C1232883011&page=' + str(page) + '&bbn=172659&keywords=television&ie=UTF8&qid=1351825075' ), headers=headers_dict)
        root = BeautifulSoup(html.text)                                      # Parse the html into something BeautifulSoup can read
        count = root.find('div',{"class" : "srSprite spr_header hdr"})
        count = count.find('h2',{"class" : "resultCount"}).text[12:14]
    link_div = root.find('div',{"id" : ("result_" + str(i))})
    print "Link " + str(i)
    link = link_div.find('a',href=True)['href'] 
    try:
        list_price = link_div.find('del',{"class" : "grey"}).text
    except:
        list_price = "None"

    get_data(link, list_price)


