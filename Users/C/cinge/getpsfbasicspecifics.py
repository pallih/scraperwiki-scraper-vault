import scraperwiki
import lxml.etree
import lxml.html
from httplib import BadStatusLine

scraperwiki.sqlite.attach("createpsflinks")
data = scraperwiki.sqlite.select("* from createpsflinks.BasicUrl order by SID")
    
def storeList (list,addr,contact):
    scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": list[0], "PIStatus":list[1], "PIEffective":list[2], "Agent":list[3],
"AgentEffective":list[4],"Notices":list[5], "Other":list[6], "AddressOne":addr[0],"AddressTwo":addr[1],"AddressThree":addr[2],
"AddressFour":addr[3],"AddressFive":addr[4],"AddressSix":addr[5],"AddressSeven":addr[6],"Phone":contact[0],"Fax":contact[1],"Email":contact[2],"Website":contact[3]},table_name='BasicInfo')

def getAddress (root):
    addressList = []
    row = root.cssselect("table.basic-information tr")[4]
    table_cells = row.cssselect("td")[0]
    xlen = len(table_cells)
    if xlen is not None:
        addressList.append (table_cells.text)
        for x in xrange(0,6):
            try:
                addressList.append(table_cells[x].tail)
            except IndexError:
                addressList.append("NULL")
    else:
        for x in xrange(0,7):          #the range is different here because we're not appending the first textline prior to entering the loop
            addressList.append("NULL")
    #print "AddressList length"+str(len(addressList))
    return addressList

def getContact (root):
    contactList = [] 
    row = root.cssselect("table.basic-information tr")[5]
    table_cells = row.cssselect("td")[0]
    if table_cells.text is not None:
        contactList.append(table_cells.text)
    else:
        contactList.append("NULL")
    #print "contactList length1"+str(len(contactList))               
    for x in xrange (0,4):
        if table_cells[x].tail is not None:
            try:
                contactList.append(table_cells[x].tail)
            except IndexError:
                contactList.append("NULL")
        else:
            contactList.append("NULL") 
    #print "contactList length2"+str(len(contactList))               
    return contactList

def getOther (root):
    otherList = []
    x = 6
    while x < 8:
        row = root.cssselect("table.basic-information tr")[x]  
        table_cells = row.cssselect("td")[0]
        if table_cells is not None:
            otherList.append(table_cells.text_content())
            x+=1
        else:
            otherList.append("NULL")
    #print "otherList length"+str(len(otherList))               
    return otherList

def grabLinks(sid, url):
    rowList = []
    rowList.append(sid)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for x in xrange(0, 4):
        row = root.cssselect("table.basic-information tr")[x]  
        table_cells = row.cssselect("td")[0]
        if table_cells is not None:
            rowList.append(table_cells.text_content())
        else:
            rowList.append("NULL")
    otherList = getOther(root)

    rowList.extend(otherList)
    #print "rowList length"+str(len(rowList))               
    list1=getAddress(root)
    list2=getContact(root)
    storeList (rowList,list1,list2)

try:
    scraperwiki.sqlite.execute("create table BasicInfo(SID string, PIStatus string, PIEffective string, Agent string, AgentEffective string, Notices string, Other string, AddressOne string, AddressTwo string, AddressThree string, AddressFour string, AddressFive string, AddressSix, AddressSeven string, Phone string, Fax string, Email string, Website string)")
    scraperwiki.sqlite.execute("create table ErrorLog(SID string, BSL string, Other string)")
except:
    print "Table already exists."


for d in data:
    try:
        grabLinks(d["SID"],d["Url"])
    except BadStatusLine:
        scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": d["SID"], "BSL": d["Firm"]}, table_name='ErrorLog')


import scraperwiki
import lxml.etree
import lxml.html
from httplib import BadStatusLine

scraperwiki.sqlite.attach("createpsflinks")
data = scraperwiki.sqlite.select("* from createpsflinks.BasicUrl order by SID")
    
def storeList (list,addr,contact):
    scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": list[0], "PIStatus":list[1], "PIEffective":list[2], "Agent":list[3],
"AgentEffective":list[4],"Notices":list[5], "Other":list[6], "AddressOne":addr[0],"AddressTwo":addr[1],"AddressThree":addr[2],
"AddressFour":addr[3],"AddressFive":addr[4],"AddressSix":addr[5],"AddressSeven":addr[6],"Phone":contact[0],"Fax":contact[1],"Email":contact[2],"Website":contact[3]},table_name='BasicInfo')

def getAddress (root):
    addressList = []
    row = root.cssselect("table.basic-information tr")[4]
    table_cells = row.cssselect("td")[0]
    xlen = len(table_cells)
    if xlen is not None:
        addressList.append (table_cells.text)
        for x in xrange(0,6):
            try:
                addressList.append(table_cells[x].tail)
            except IndexError:
                addressList.append("NULL")
    else:
        for x in xrange(0,7):          #the range is different here because we're not appending the first textline prior to entering the loop
            addressList.append("NULL")
    #print "AddressList length"+str(len(addressList))
    return addressList

def getContact (root):
    contactList = [] 
    row = root.cssselect("table.basic-information tr")[5]
    table_cells = row.cssselect("td")[0]
    if table_cells.text is not None:
        contactList.append(table_cells.text)
    else:
        contactList.append("NULL")
    #print "contactList length1"+str(len(contactList))               
    for x in xrange (0,4):
        if table_cells[x].tail is not None:
            try:
                contactList.append(table_cells[x].tail)
            except IndexError:
                contactList.append("NULL")
        else:
            contactList.append("NULL") 
    #print "contactList length2"+str(len(contactList))               
    return contactList

def getOther (root):
    otherList = []
    x = 6
    while x < 8:
        row = root.cssselect("table.basic-information tr")[x]  
        table_cells = row.cssselect("td")[0]
        if table_cells is not None:
            otherList.append(table_cells.text_content())
            x+=1
        else:
            otherList.append("NULL")
    #print "otherList length"+str(len(otherList))               
    return otherList

def grabLinks(sid, url):
    rowList = []
    rowList.append(sid)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for x in xrange(0, 4):
        row = root.cssselect("table.basic-information tr")[x]  
        table_cells = row.cssselect("td")[0]
        if table_cells is not None:
            rowList.append(table_cells.text_content())
        else:
            rowList.append("NULL")
    otherList = getOther(root)

    rowList.extend(otherList)
    #print "rowList length"+str(len(rowList))               
    list1=getAddress(root)
    list2=getContact(root)
    storeList (rowList,list1,list2)

try:
    scraperwiki.sqlite.execute("create table BasicInfo(SID string, PIStatus string, PIEffective string, Agent string, AgentEffective string, Notices string, Other string, AddressOne string, AddressTwo string, AddressThree string, AddressFour string, AddressFive string, AddressSix, AddressSeven string, Phone string, Fax string, Email string, Website string)")
    scraperwiki.sqlite.execute("create table ErrorLog(SID string, BSL string, Other string)")
except:
    print "Table already exists."


for d in data:
    try:
        grabLinks(d["SID"],d["Url"])
    except BadStatusLine:
        scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": d["SID"], "BSL": d["Firm"]}, table_name='ErrorLog')


