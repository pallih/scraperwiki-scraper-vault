import scraperwiki
import lxml.etree
import lxml.html
from httplib import BadStatusLine

scraperwiki.sqlite.attach("testscraper_6")
data = scraperwiki.sqlite.select("* from testscraper_6.Firms order by SID")
contactList = []

def regFind(str):    
    m=pregex.search(str)
    if m is not None:
        return m.group()

def storeList (list,addr, contact):
    scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": list[0], "Status":list[1], "Effective":list[2], "TiedAgent":list[3],
"InsuranceMediation":list[4], "LaunderingRegistered":list[5], "Notices":list[6], "Other":list[7], "AddressOne":addr[0],"AddressTwo":addr[1],"AddressThree":addr[2],
"AddressFour":addr[3],"Phone":contact[0],"Fax":contact[1],"Email":contact[2],"Website":contact[3]},table_name='BasicInfo')

def getAddress (root):
    addressList = []
    row = root.cssselect("table.basic-information1 tr")[5]
    table_cells = row.cssselect("td")[0]
    xlen = len(table_cells)
    if xlen is not None:
        addressList.append (table_cells.text)
        for x in xrange(0,3):
            try:
                addressList.append(table_cells[x].tail)
            except IndexError:
                addressList.append("NULL")
    else:
        for x in xrange(0,3):
            addressList.append("NULL")

    return addressList

def getContact (root):
    contactList = [] 
    row = root.cssselect("table.basic-information1 tr")[6]
    table_cells = row.cssselect("td")[0]
    if table_cells.text is not None:
        contactList.append(table_cells.text)
        for x in xrange (0,3):
            if table_cells[x].tail is not None:
                try:
                    contactList.append(table_cells[x].tail)
                except IndexError:
                    contactList.append("NULL")
            else:
                contactList.append("NULL")                
    else:
        for x in xrange (0,3):
            contactList.append("NULL")

    return contactList

def getOther (root):
    otherList = []
    x = 7
    while x < 9:
        row = root.cssselect("table.basic-information1 tr")[x]  
        table_cells = row.cssselect("td")[0]
        otherList.append(table_cells.text_content())
        x+=1
    return otherList

def grabLinks(firm, sid):
    rowList = []
    rowList.append(sid)
    html = scraperwiki.scrape(firm)
    root = lxml.html.fromstring(html)
    for x in xrange(0, 5):
        row = root.cssselect("table.basic-information1 tr")[x]  
        table_cells = row.cssselect("td")[0]
        rowList.append(table_cells.text_content())
    otherList = getOther(root)
    rowList.extend(otherList)
    list1=getAddress(root)
    list2=getContact(root)
    storeList (rowList,list1,list2)

try:
    scraperwiki.sqlite.execute("create table BasicInfo(SID string, Status string, Effective string, TiedAgent string, InsuranceMediation string, LaunderingRegistered string, Notices string, Other string, AddressOne string, AddressTwo string, AddressThree string, AddressFour string, Phone string, Fax string, Email string, Website string)")
    scraperwiki.sqlite.execute("create table ErrorLog(SID string, BSL string, Other string)")

except:
    print "Table already exists."

for d in data:
    try:
        grabLinks(d["Firm"],d["SID"])
    except BadStatusLine:
        scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": d["SID"], "BSL": d["Firm"]})
