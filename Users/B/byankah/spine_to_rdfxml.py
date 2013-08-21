import scraperwiki

import scraperwiki  
import re
import scrapemark
from BeautifulSoup import BeautifulSoup          

def getEachRecord(name, urlz):
    #print url
    #html = scraperwiki.scrape(url)
    #soup = BeautifulSoup(html)
    #date = soup.find(text="Date Completed").parent.parent.parent.nextSibling.nextSibling.text
    #print date
    inventory = {}
    temp = scrapemark.scrape("""
        {*
    <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;" face="Verdana"><em>Date Completed</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ date }}</font>
        *}
        """,
        url=urlz)
    inventory['date'] = temp['date']
    temp = scrapemark.scrape("""
        {*
    <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;" face="Verdana"><em>Copyright</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ copyright }}</font>
        *}
        """,
        url=urlz)
    inventory['copyright'] = temp['copyright']
    temp = scrapemark.scrape("""
        {*
    <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Process Type</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>

        *}
        """,
        url=urlz)
    inventory['description'] = temp['desc']
    temp = scrapemark.scrape("""
        {*
    <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Function</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>

        *}
        """,
        url=urlz)
    inventory['description'] = inventory['description'] + ". " + temp['desc']
    scraperwiki.sqlite.execute("insert into SPINE values (?,?,?,?)", (name,inventory['date'],inventory['description'],inventory['copyright']))
    scraperwiki.sqlite.commit()     


def getIO(name, urlz):
    #print url
    #html = scraperwiki.scrape(url)
    #soup = BeautifulSoup(html)
    ios = scrapemark.scrape("""
        {*

    <td><font>{{ [io].direction }}</font></td>
    <td><font>{{ [io].ft }}</font></td>
    <td><font>{{ [io].substance }}</font></td>
    <td>{{ [io].value }}</font></td>
    <td>{{ [io].min }}</td>
    <td>{{ [io].max }}</td>
    <td>{{ [io].std }}</td>
    <td><font>{{ [io].unit }}</font></td>
    <td><font>{{ [io].environment }}</font></td>
    <td><font>{{ [io].geo }}</font></td>
    </tr>
        *}
        """,
        url=urlz)
    for flow in ios['io']:
        if flow['direction'] == "Input" or flow['direction'] == "Output":
            scraperwiki.sqlite.execute("insert into SPINEIO values (?,?,?,?,?,?,?,?,?,?,?)", (name,flow['direction'],flow['ft'],flow['substance'],flow['value'],flow['min'],flow['max'],flow['std'],flow['unit'],flow['environment'],flow['geo']))
            scraperwiki.sqlite.commit() 

try:           
    scraperwiki.sqlite.execute("select * from SPINE")
except scraperwiki.sqlite.SqliteError, e:
    scraperwiki.sqlite.execute("create table SPINE ('name','description','date','copyright')")       
try:           
    scraperwiki.sqlite.execute("select * from SPINEIO")
except scraperwiki.sqlite.SqliteError, e:
    scraperwiki.sqlite.execute("create table SPINEIO ('product','Direction','FlowType','Substance','Quantity','Min','Max','SDev','Unit','Environment','Geography')")       
rooturl = "http://cpmdatabase.cpm.chalmers.se/Scripts/"         
html = scraperwiki.scrape("http://cpmdatabase.cpm.chalmers.se/Scripts/General.asp?QBase=Process")
soup = BeautifulSoup(html)
pages = soup.findAll(attrs={'href' : re.compile("sheet.asp\?ActId=*.")});
#testpage = "http://cpmdatabase.cpm.chalmers.se/Scripts/sheet.asp?ActId=ECOP3225"
for p in pages:
    fullurl = rooturl + p['href']
    getEachRecord(p.parent.parent.contents[3].text,fullurl.replace(" ", "%20"))
    getIO(p.parent.parent.contents[3].text,fullurl.replace(" ", "%20"))