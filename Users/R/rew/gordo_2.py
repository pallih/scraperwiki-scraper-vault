import scraperwiki

import scraperwiki

# Helping https://scraperwiki.com/scrapers/gordo
# Currently this scrapes div id="detailtext" in each page
# Needs to be refined so that you're grabbing <b> and <br/> tags within that - or regex?
# Also needs simplifying/renaming of variables/comments etc.

#If you want to understand this scraper - start at the bottom where it says 'base_url' (line 52 or so)

import scraperwiki
#import urlparse
import lxml.html

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Use cssselect to find the contents of a particular HTML tag, and put it in a new object 'rows'
    #there's more than one table, so we need to specify the class="destinations", represented by the full stop
    rows = root.cssselect("div#detailtext")
    for row in rows:
        #Create a new empty record
        record = {}
            #Put the contents of the first <td> into a record in the column 'FSM'
        record['FSM'] = row.text_content()
            #this takes the ID number, which has been named item in the for loop below
        record['ID'] = item
        print record, '------------'
            #Save in the SQLite database, with the ID code to be used as the unique reference
        scraperwiki.sqlite.save(["ID"], record)


#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    print html
    #now we use the lxml.html function imported above to convert 'html' into a new object, 'root'
    root = lxml.html.fromstring(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://marinetraffic.com/ais/shipdetails.aspx?MMSI='
#And these are the numbers which we need to complete that URL to make each individual URL
#This list has been compiled using the =JOIN formula in Google Docs on a column of mmsi numbers
schoolIDs = ['205059000',    '205106000',    '205149000',    '205153000',    '205162000',    '205169000',    '205192000',    '205197000',    '205227000',    '205237000',    '205241000',    '205243000',    '205246000',    '205262000',    '205284000',    '205306000',    '205316000',    '205321000',    '205322000',    '205333000',    '205345000',    '205378000',    '205543000',    '209093000',    '215464000',    '215870000',    '219088000',    '219248000',    '219255000',    '219260000',    '219261000',    '219482000',    '220052000',    '220235000',    '220479000',    '231710000',    '231734000',    '231754000',    '232003278',    '232003395',    '232003451',    '232003506',    '232003758',    '232003832',    '232004633',    '232007860',    '233296000',    '234450000',    '235000826',    '235000928',    '235001055',    '235005510',    '235005640',    '235005820',    '235007100',    '235007785',    '235007827',    '235008024',    '235008061',    '235008229',    '235008317',    '235009880',    '235009920',    '235010110',    '235012823',    '235015000',    '235015717',    '235016787',    '235017728',    '235018021',    '235019133',    '235019819',    '235020127',    '235020249',    '235021707',    '235024029',    '235024127',    '235026097',    '235029148',    '235033039',    '235034317',    '235037067',    '235051181',    '235051182',    '235055159',    '235055509',    '235055537',    '235058808',    '235058809',    '235059319',    '235059964',    '235059973',    '235060252',    '235061961',    '235062227',    '235063728',    '235063849',    '235063852',    '235063854',    '235066014',    '235066353',    '235067991',    '235068109',    '235068112',    '235068336',    '235068455',    '235069182',    '235069806',    '235072422',    '235076464',    '235076657',    '235076857',    '235078722',    '235081182',    '235084022',    '235087113',    '235087214',    '235087431',    '235089094',    '235090186',    '235091051',    '235091052',    '235091787',    '235093823',    '235093892',    '235094956',    '235096456',    '235096796',    '235096924',    '235097044',    '235098051',    '235099855',    '235192000',    '235627000',    '235899912',    '236083000',    '236175000',    '236246000',    '236260000',    '236401000',    '240592000',    '240602000',    '241035000',    '244089000',    '244285000',    '244630048',    '244650023',    '244670071',    '244734000',    '244750860',    '244843000',    '245573000',    '245610000',    '246257000',    '246295000',    '246541000',    '248594000',    '248730000',    '249231000',    '249344000',    '250001877',    '250108540',    '255802940',    '255803880',    '255804750',    '256210000',    '256495000',    '256775000',    '256787000',    '256788000',    '258112320',    '258127920',    '265673340',    '273351390',    '308847000',    '309225000',    '311027600',    '311027700',    '311758000',    '319194000',    '355284000',    '355704000',    '413089000',    '477115900',    '477173500',    '477238000',    '477434900',    '477627200',    '477786500',    '538002073',    '538002773',    '538002883',    '538003293',    '538003326',    '538003346',    '538003356',    '538003365',    '538003629',    '538004388',    '538004532',    '548796000',    '565637000',    '565639000',    '636011392',    '636014088',    '636015000',    '636015106',    '636091582',    '636091593',
]

#go through the schoolIDs list above, and for each ID...
for item in schoolIDs:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)
