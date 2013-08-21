import scraperwiki
import mechanize
import re
import lxml.html
from lxml import etree
from BeautifulSoup import BeautifulSoup



def scrape(html,tbl='tmp'):
    #soup = BeautifulSoup(html)
    #<tr class="ResultRow">
    root = lxml.html.fromstring(html)
    rows=root.findall('.//tr[@class="ResultRow"]')
    #print 'a',rows,len(rows)
    bigdata=[]
    for row in rows:
        name=row.find('.//div[@class="ResultsBusinessName"]/a').text
        '''
        <input type="hidden" class="ResultsFHRSID" value="3142" />
                                    <input type="hidden" class="ResultsLongitude" value="-1.166279" />
                                    <input type="hidden" class="ResultsLatitude" value="50.72615" />
                                    <a href="/business/en-GB/3142">
                                        Abingdon Lodge</a>
                                </div>
                                <div class="ResultsBusinessAddress">
                                    
20a West Street
Ryde
Isle Of Wight

                                </div>
                                <div class="ResultsBusinessPostcode">

        <td class="ResultsRatingValue">
                            <div class="columnPadding">
                                <img src="/images/scores/small/fhrs_4_en-GB.JPG"
                                    alt="Food hygiene rating is '4': Good" title="Food hygiene rating is '4': Good" />
                            </div>
                        </td>
                        <td class="ResultsRatingDate">
                            <div class="columnPadding">
        '''
        bid=row.find('.//input[@class="ResultsFHRSID"]').get('value')
        clat=row.find('.//input[@class="ResultsLatitude"]').get('value')
        clong=row.find('.//input[@class="ResultsLongitude"]').get('value')
        postcode=row.find('.//div[@class="ResultsBusinessPostcode"]').text
        addr=row.find('.//div[@class="ResultsBusinessAddress"]').text
        rating=row.find('.//td[@class="ResultsRatingValue"]/div[@class="columnPadding"]/img').get('alt')
        rating=rating.replace('Food hygiene rating is ','')
        date=row.find('.//td[@class="ResultsRatingDate"]/div[@class="columnPadding"]').text
        #print name,bid,addr,postcode,rating,date,clat,clong
        littledata={'name':name,'bid':bid,'addr':addr,'postcode':postcode,'rating':rating,'date':date,'clat':clat,'clong':clong}
        bigdata.append(littledata.copy())
    scraperwiki.sqlite.save(unique_keys=["bid","date"], table_name=tbl, data=bigdata)

def runner(response,br,tbl):
    #print(response)
    #scrape(response,tbl)
    #root = lxml.html.fromstring(response)
    #current_page = int(root.xpath ('//span[@id="SearchResults_uxPagesPage"]')[0].text)
    #total_pages = int(root.xpath ('//span[@id="SearchResults_uxPagesCount"]')[0].text)
    #print current_page,total_pages
    #br.form = list(br.forms())[0]
    #br.select_form(nr=0)
    #if current_page<total_pages:
    running=1
    while running!=-1:
        print current_page,total_pages
        scrape(response,tbl)
        br.select_form(nr=0)
        response = br.submit(name='ctl00$SearchResults$uxPagerNext').read()  #"Press" the next submit button
        root = lxml.html.fromstring(response)
        current_page = int(root.xpath ('//span[@id="SearchResults_uxPagesPage"]')[0].text)
        total_pages = int(root.xpath ('//span[@id="SearchResults_uxPagesCount"]')[0].text)
        if current_page>=total_pages: running=-1
        #runner(response,br,tbl)

#I have hardcoded the root URL for a search on a specific local authority  
'''
url='http://ratings.food.gov.uk/enhanced-search/en-GB/%5E/%5E/alpha/0/867/%5E/0/1/10'
area='Isle Of Wight'

br = mechanize.Browser()
br.open(url)
response = br.response().read()

runner(response,br,area.replace(' ',''))
'''


url='http://ratings.food.gov.uk/enhanced-search/en-GB/%5E/%5E/alpha/7844/221/%5E/0/1/10'
area='Lincoln City Takeaways'

br = mechanize.Browser()
br.open(url)
response = br.response().read()

runner(response,br,area.replace(' ',''))


'''
#FROM a previous version of the FSA website

#The Food Ratings Agency results appear to be capped at 100 pages even if there are more results
#Way round this is to generate an advanced query that returns < 100 pages of results, then do several queries
#Run an advanced search query then paste the URL below
#If you search by local authority, it focusses the search more effectively than searching for e.g. Wight

# Thanks to Páll Hilmarsson for spotting how to do the "Next>" click...
#   Test example here: http://scraperwiki.com/scrapers/test-food-standards-pagination/edit/

#url = 'http://ratings.food.gov.uk/AdvancedSearch.aspx?s=1&so=Equal&st=1&bt=5&las=284'
#url="http://ratings.food.gov.uk/AdvancedSearch.aspx?s=5&so=Equal&st=1&bt=12&las=284"
#url='http://ratings.food.gov.uk/QuickSearch.aspx?q=po30'
url='http://ratings.food.gov.uk/enhanced-search/en-GB/%5E/%5E/alpha/0/867/%5E/0/1/10'

#Note the the results appear to contain lots of duplicate entries?
#If the scraper sees a duplicate facility ID, it uses the current data and overwrites the original data

#If you run the scraper several times with different URLs, it should build up the database.

#Some bits of the page also appear to drop into Welsh every so often?!
# (This was a result of me "clicking" the 'swtich to welsh' form submit button


#The next step would be to scrape the individual record pages to enrich the data for each entry


#-----NO NEED TO GO ANY FURTHER----------



#---- script cribbed from tutorial
# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

def scrape(html,typ):
        print "In scraper..."
        #html = response.read()
        #print html
        #print "Clinicians found:", re.findall("PDetails.aspx\?ProviderId.*?>(.*?)</a>", html)
        soup = BeautifulSoup(html)
        try:
            rows = soup.find('table', {'class':'uxMainResults'}).findAll('tr')
        except: rows=[]
        for row in rows[1:]:
            #print row
            #looking for: resultID, name, address, postcode, rating
            cells=row.findAll('td')
            id=cells[0].find('div',{'class':'resultID'}).string
            id=id.strip()
            if hasattr(cells[0], 'a'):
                    name = cells[0].a.string
            else: name='UNKOWN'
            #i wonder? cascade a continue here if any lookup fails?
            address=cells[1].find('div',{'class':'resultAddress'}).string
            address=address.strip()
            postcode=cells[2].find('div',{'class':'resultPostcode'}).string
            postcode=postcode.strip()
            rating=cells[3].find('img').get('title')
            #for some reason this appears to drop into Welsh every so often?!
            #maybe build a lookup/rewriter to throw it back into English?
            # maybe also just pull out the rating number? eg
            rv=re.search(".*'(\d+)'.*",rating)
            if rv: ratingval=rv.group(1)
            else: ratingval=''
            #print id, name, address, postcode, rating,ratingval,typ
            scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id, "name":name,'addr':address,'postcode':postcode,'rating':rating,'ratingval':ratingval,'typ':typ})
        return len(rows)

def loader(br,url,typ=''):
    #br = mechanize.Browser()
    #cribbed from Páll Hilmarsson: http://scraperwiki.com/scrapers/test-food-standards-pagination/edit/
    br.open(url)
    response = br.response().read()
    print(response)
    root = lxml.html.fromstring(response)
    try:
        current_page = root.xpath ('//span[@id="ctl00_ContentPlaceHolder1_uxResults_uxCurrentPage"]/.')
        current_page = int(current_page[0].text)
        total_pages = root.xpath ('//span[@id="ctl00_ContentPlaceHolder1_uxResults_uxPageCount"]/.')
        total_pages = int(total_pages[0].text)
        print 'zz',root.xpath ('//div[@id="pagingTotal"]/span')
        current_page = root.xpath ('//div[@id="pagingTotal"]/span')[0].text
        total_pages = root.xpath ('//div[@id="pagingTotal"]/span')[1].text
    except:
        current_page = 0
        total_pages = 0
    print 'Total pages: ', total_pages
    print 'Current page: ', current_page

    scrape(response,typ)
    
    while current_page<total_pages:
        current_page=current_page+1
        print "Page ",current_page,' of ',total_pages
        br.select_form(nr=0)
        #br.form.set_all_readonly(False)
        #br['__EVENTTARGET'] = ''
        #br['__EVENTARGUMENT'] = ''
        print 'Fetching next results page',
        response = br.submit(name='ctl00$ContentPlaceHolder1$uxResults$uxNext').read()  #"Press" the next submit button
        scrape(response,typ)
    return
#original()


def runner():
    br = mechanize.Browser()
    # sometimes the server is sensitive to this information
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    s= [0,1,2,3]#[0,1,2,3,4,5]
    btype=[10]#[7,2,14,13,12,72,8,1,6,9,11,3,4,10,5]
    typeTyp={"7":"Distributors/Transporters","2":"Hotel/Guest House","14":"Importers/Exporters","13":"Manufacturers and Packers","12":"Mobile Food Unit","72":"Primary Producers","8":"Pub/Club","1":"Restaurant/Cafe/Canteen","6":"Restaurants and Caterers - Other","9":"Retailer - Other","11":"School/College","3":"Small Retailer","4":"Supermarket/Hypermarket","10":"Take-Away","5":"Caring Premises"}
    for rating in s:
        for fac in btype:
            url="http://ratings.food.gov.uk/AdvancedSearch.aspx?s="+str(rating)+"&so=Equal&st=1&bt="+str(fac)+"&las=284"
            typ=typeTyp[str(fac)]
            print "Loading",typ,rating
            loader(br,url,typ)

#runner()
'''