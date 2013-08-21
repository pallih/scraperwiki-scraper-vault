###############################################################################
# To do list:
# - other postings by same account
# - use date comparison instead of URL comparison for last_link
# - keyword determination
# - eliminate duplicate phone numbers
# - scrape price
#
# External druthers:
# - photos themselves
# - other pages with same phone number
# - add a Names Corpus, preferably with additions for names common here.
###############################################################################
import time
import re                           # Regular expression library
import scraperwiki                  # Scraperwiki's library. 
import urlparse                     # Allows URL parsing. Currently unused.
import lxml.html                    # xml/html parsing library
from lxml.cssselect import CSSSelector # parses based on tags
from lxml.html.clean import Cleaner # To get rid of unneeded HTML tags
from datetime import datetime, date                       # time is on my side. (date operations)
import codecs
import base64
import urllib

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

NEIGHBORHOODS = ['queens', 'manhattan', 'westchester', 'bronx', 'long island', 'midtown east', ' midtown west', 'brooklyn', 'harlem', 'chinatown', 'east side', 'fairfield', 'jersey', 'college point', 'jamaica', 'laurel,' 'rockville', 'fairfax', 'tyson', 'capitol hill', 'college park', 'greenbelt']

# Dictionary to replace common phone number obfuscations with numbers
wordDic = {
'ten': '10',
'eleven': '11',
'twelve': '12',
'thirteen': '13',
'fourteen': '14',
'fifteen': '15',
'sixteen': '16',
'seventeen': '17',
'eighteen': '18',
'nineteen': '19',
'one': '1',
'two': '2',
'three': '3',
'four': '4',
'five': '5',
'six': '6',
'seven': '7',
'eight': '8',
'nine': '9',
'zero': '0',
'oh': '0',
'o': '0'}

# Dictionary to replace common alphanumeric obfuscations with letters.
subDic = {
'¢': 'c',
'¥': 'Y',
'€': 'E',
'§': 'S',
'©': 'c',
'®': 'r',
'†': 'T',
'Â': 'A',
'Õ': 'O',
'¡': 'I',
'Ø': 'O',
'ø': 'o',
'ß': 'B',
'@': 'a',
'£': 'E'}

# not currently used.
def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)

# scrape_table function: gets passed an individual page to scrape
def scrape_links(links):
     maincleaner = Cleaner(allow_tags=['div'], remove_unknown_tags=False, remove_tags=['div'])     # funtion to remove every tag

#    while True:
     for link in links:            # Loop through all the links
        if link == last_link:      # Check if this link has already been scraped (this will eventually be changed to check dates)
            break                  # If we've hit something we've already scraped, break out of the loop
#        try:
        linkhtml = scraperwiki.scrape(link).decode('latin_1')          # scrape the contents of the current link and decode from Windows-1252 encoding
        print link
        root = lxml.html.fromstring(linkhtml)                               # turn scraped content into an HTML object

        # GET TITLE
        title = root.cssselect("h1")[0].text.encode('utf-8')                # grab the page header (title) and return its text as unicode
        title = replace_all(title, subDic)                                  # replace alphanumeric obfuscations with letters

        # GET DATE
        date = root.cssselect("div.adInfo")[0].text                         # get the text of the html entity that contains the date and time of the post
        cleandate = re.sub(r'(\S+\s+\d+,\s+\d\d\d\d)(?:,?) (\d+\:\d+ \w\w)', r'\1 \2', date.strip())  # get date into a standard format
        cleandate = re.search(r'\S+\s+\d+, \d\d\d\d \d+\:\d+ \w\w', cleandate).group(0) # find the date string on the page
        rawdate = datetime.strptime(cleandate,'%B %d, %Y %I:%M %p')                 # encode the date as a date using format Month dd, YYYY
        date = rawdate.strftime('%Y-%m-%d %H:%M')                        # decode that date back into a string of format YYYY-mm-dd

        # GET MAIN BODY TEXT
        mainwithtags = root.cssselect("div.postingBody")[0]                # grabs the body text of the post
        main = maincleaner.clean_html(mainwithtags).text.encode('utf-8')            # gets rid of all HTML tags
        main = replace_all(main, subDic)                                            # replace alphanumeric obfuscations with letters

        # GET PHONE NUMBER(S)
        stripped = replace_all(main.lower(), wordDic)                               # replaces common phone number obfuscations with actual numbers
        phonecomp = re.compile("[\s\-/=\.,{}_\!\@\#\$\%\^\&\*\(\)\~]")      # list of known phone number dividers
        stripped = phonecomp.sub('',stripped)                               # remove phone number dividers
        phone = re.findall(r'(?:1?)[1-9]\d{9}',stripped)                    # search for groups of 10 consecutive numbers (with an optional preceding 1)
        phone = list(set(phone))                                            # gets rid of duplicate numbers by turning list into a set and back
        phone = ", ".join(phone)                                            # formats phone numbers as "phone1, phone2,... phoneN"
        
        # GET LISTED AGE
        if root.cssselect("p.metaInfoDisplay"):                             # does the entry have metainfo?
            listedage = root.cssselect("p.metaInfoDisplay")[0]              # get the the first html metainfo element
            listedage = re.sub("[^\d]","",listedage.text)                   # get rid of all non-numeric text in the text of the element
        else:                                                               # if there's no metainfo
            listedage = ""                                                  # set the listed age to an empty string

        # GET LOCATION
        if re.findall(r'Location\:(.*?)\</div\>',linkhtml, flags=re.DOTALL):  # 
            location = re.findall('Location\:(.*?)\</div\>',linkhtml, flags=re.DOTALL)[0].encode('utf-8')
#            location = removeNonAscii(location)
            #if any(x in NEIGHBORHOODS) in location:
             #   print x, 'x'
              #  area =  x
            area = None
            for neighborhood in NEIGHBORHOODS:
                if neighborhood in location.lower():
                    area = neighborhood

            print repr(area)
            print repr(location)
        else:
            location = ""

        picturelist=[]
        pictures = root.cssselect('ul#viewAdPhotoLayout img')
        print pictures
        if pictures:
            largepic = None
            for i in range(len(pictures)):
                largepic = re.sub('/medium/','/large/',pictures[i].get('src'))
                picturelist.append(largepic)
            print picturelist 
            picturelist = " ".join(picturelist)
            x = urllib.urlopen(largepic).read()
            piccode = base64.encodestring(x)
            print piccode
        else:
            piccode = None
        
#        except:
#            print 'FAILED TO LOAD: ' + link
#        continue
#            record = {}
#            record['Title'] = 'LOAD FAILURE'
        # Set up our data record - we'll need it later

        record = {}
        record['Title'] = title #.encode('ascii', 'ignore').strip()
        record['Date'] = date
        record['Main'] = main #.encode('ascii', 'ignore').strip()
        record['Pictures'] = picturelist
        record['Phone'] = phone
        record['Listed Age'] = listedage #.encode('ascii', 'ignore').strip()
        record['Location'] = location
        record['area']= area
        record['PicCode'] = piccode #.encode('ascii', 'ignore').strip()
            # Print out the data we've gathered
           #print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["Title"], record)
        time.sleep(5)

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    html = re.sub('\<a(?:.*?)resultsSectionLabel(?:.*?)/a\>','',html)
#    print html
    root = lxml.html.fromstring(html)
    sel = CSSSelector('div.cat a')
    links = [a.get('href') for a in sel(root)]
    print links
#    print links
    scrape_links(links)
    scraperwiki.sqlite.save_var('last_link', links[0])
    scraperwiki.sqlite.save_var('dclastlink', links[0])
    next_link = root.cssselect("a.next")
#    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
#        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
#scraperwiki.sqlite.get_var('last_link'):
#scraperwiki.sqlite.execute("UPDATE `swdata` SET Region = 'DC' WHERE Region IS NULL;")
print "Hello!"
print datetime.now()
scraperwiki.sqlite.save_var('lastcheck', datetime.now().strftime('%c'))
if scraperwiki.sqlite.get_var('last_link') == None:
    last_link = ""
else:
    last_link = scraperwiki.sqlite.get_var('last_link')

base_url = 'http://newjersey.backpage.com/adult/'
#starting_url = urlparse.urljoin(base_url, 'example_table_1.html')
scrape_and_look_for_next_link(base_url)
