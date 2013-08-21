import scraperwiki
import lxml.html
#We're going to load HTML pages in as DOM trees

#This is a really useful utility function that gets "flat" text from within a (set of) tags.
def flatten(el):           
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)

#This function scrapes an individual record page for each company in the IW Chamber of Commerce
#We pass it the path to the specific page
def scrapeItem(path):
    #Constrcut the page URL from the path
    url='http://www.iwchamber.co.uk'+path
    #Grab the page
    fhtml = scraperwiki.scrape(url)
    froot = lxml.html.fromstring(fhtml)
    #The data is held within the rows of a single table, so we can just grab a list of all the rows
    rows=froot.xpath('.//tr')
    data={}
    #Go through each row one at a time.
    #The cell name is in the single <th> element within the row, the value within the single <td> element
    #So for example, each row looks like this:
    '''
    <tr class="alt">
      <th>Business Type(s):</th>
      <td>Education</td>
    </tr>
    '''
    #Iterate through each row (becomes an attribute in the record array for this company) one at a time
    for row in rows:
        #Have a cursory attempt at tidying up some of the messiness (I didn't check any of the tidying worked! ?May need to double escape chars?)
        data[ flatten(row.xpath('th')[0]).strip(':').replace('(s)','') ] = flatten(row.xpath('td')[0]).replace('\r\n',' ').strip()
    #Save the data into the scraperwiki database
    scraperwiki.sqlite.save(unique_keys=['Company name'], table_name='indexData', data=data.copy())

#The page that lists all the IW Chamber members
url='http://www.iwchamber.co.uk/members'
#Grab it
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
#The single table has a each company described within in a separate <th> element, so grab them all
#So for example, each row looks something approximately like this:
'''
    <tr  >
            <th>
                <a href="/members/?id=965">Bembridge Windmill</a>
            </th>
            <td>
                Attractions                &nbsp;
            </td>
        </tr>
'''
items=root.xpath('.//th')
#For each company row turn...
for item in items:
    #Grab the path to its data page and scrape it
    scrapeItem(item.xpath('a/@href')[0])
