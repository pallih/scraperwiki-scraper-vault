import scraperwiki  
import re
import scrapemark
from BeautifulSoup import BeautifulSoup          

def getEachRecord(name, urlz):
    inventory = {}
    meta = {}
    desc = {}
    meta['description'] = ""

    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Intended User</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    meta['description'] = meta['description'] + " Intended User: " + temp['desc']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>General Purpose</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc']
    except NameError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Detailed Purpose</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc']
    except NameError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Commissioner</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    meta['description'] = meta['description'] + temp['desc']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Practitioner</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc']   
    except NameError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Reviewer</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Applicability </em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>About Data</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Administrating organization</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Financier</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Data documentor</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Review committee for imported data:</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Notes</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Year</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ year }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['year'] = temp['year'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Publication</em></font></th>

    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ publication }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['publication'] = temp['publication']
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
    <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;" face="Verdana"><em>Date Completed</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ date }}</font>
        *}
        """,
        url=urlz)
    try:
        inventory['date'] = temp['date']
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
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

    functionalunit = 
    temp = scrapemark.scrape("""
        {*
<td valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em><a name="Functional Unit"><strong>Functional Unit</strong></a><br>
    (see also <a href="#Functional Unit Explanation">Functional Unit
    Explanation</a>)</em></font></font></td>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    functionalunit = temp['desc']
    fulluri = 'http://footprinted.org/rdfspace/lca/' + name
    lcistr = '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:eco="http://ontology.earthster.org/eco/core#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"><rdf:Description rdf:about="http://footprinted.org/rdfspace/lca/' + name + '"><rdfs:type rdf:resource="http://ontology.earthster.org/eco/core#LCAModel"/>'
    lcistr = lcistr + '<rdfs:label rdf:resource="' + name + '"/>'      
    lcistr = lcistr + '<eco:models rdf:nodeID="process' + urlz + '"/>' 
    lcistr = lcistr + getIO(name, urlz)
    lcistr = lcistr +  "</rdf:Description></rdf:RDF>"
    scraperwiki.sqlite.execute("insert into SPINE values (?,?,?)", (urlz, fulluri,lcistr))
    scraperwiki.sqlite.commit() 
    #publication
    num = "1";
    biburi = "http://footprinted.org/rdfspace/bibliography/" + num
    bibrdf = "<rdf:RDF><rdf:Description><rdf:about>http://footprinted.org/rdfspace/bibliography/" + num + "</rdf:about><dc:title>" + meta['publication'] + "</dc:title></rdf:Description></rdf:RDF>"
    scraperwiki.sqlite.execute("insert into SPINE values (?,?,?)", (urlz, biburi,bibrdf))
    scraperwiki.sqlite.commit() 

def getIO(name, urlz):
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
    inventorystr = ""
    for flow in ios['io']:
        if flow['direction'] == "Input" or flow['direction'] == "Output":
            inventorystr = inventorystr + "<eco:hasUnallocatedExchange>";
            inventorystr = inventorystr + '<eco:hasEffect><rdfs:type rdf:resource="eco:' + flow['direction'] + '" /><eco:hasTransferable><eco:Substance><rdfs:label>' + flow['substance'] + '</rdfs:label></eco:Substance></eco:hasTransferable></eco:hasEffect>'
            inventorystr = inventorystr + "<eco:hasQuantity><eco:hasUnitOfMeasure>" + flow["unit"] + "</eco:hasUnitOfMeasure><eco:hasMagnitude>" + flow["value"] + "</eco:hasMagnitude><ecoUD:maxValue>" + flow["max"] + "</ecoUD:maxValue><ecoUD:minValue>" + flow["min"] + "</ecoUD:minValue><ecoUD:maxValue>" + flow["max"] + "</ecoUD:maxValue><ecoUD:ecoUD:standardDeviation95>" + flow["std"] + "</ecoUS:ecoUD:standardDeviation95></eco:hasQuantity>";
            inventorystr = inventorystr + '</eco:hasUnallocatedExchange>';
    return inventorystr

# Main
# http://cpmdatabase.cpm.chalmers.se/Scripts/sheet.asp?ActId=KI-2010-06-23-129
try:           
    scraperwiki.sqlite.execute("select * from SPINE")
except scraperwiki.sqlite.SqliteError, e:
    scraperwiki.sqlite.execute("create table SPINE ('spineurl','uri','rdf')")      
#scraperwiki.utils.httpresponseheader( "Content-Type", "text/xml")
rooturl = "http://cpmdatabase.cpm.chalmers.se/Scripts/"         
html = scraperwiki.scrape("http://cpmdatabase.cpm.chalmers.se/Scripts/General.asp?QBase=Process")
soup = BeautifulSoup(html)
pages = soup.findAll(attrs={'href' : re.compile("sheet.asp\?ActId=*.")});
#testpage = "http://cpmdatabase.cpm.chalmers.se/Scripts/sheet.asp?ActId=ECOP3225"
x = 1;
for p in pages:
    fullurl = rooturl + p['href']
    getEachRecord(p.parent.parent.contents[3].text,fullurl.replace(" ", "%20"))
    x = x +1
    if x == 2:
        exitimport scraperwiki  
import re
import scrapemark
from BeautifulSoup import BeautifulSoup          

def getEachRecord(name, urlz):
    inventory = {}
    meta = {}
    desc = {}
    meta['description'] = ""

    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Intended User</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    meta['description'] = meta['description'] + " Intended User: " + temp['desc']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>General Purpose</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc']
    except NameError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Detailed Purpose</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc']
    except NameError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Commissioner</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    meta['description'] = meta['description'] + temp['desc']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Practitioner</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc']   
    except NameError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Reviewer</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Applicability </em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>About Data</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Administrating organization</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Financier</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Data documentor</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Review committee for imported data:</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Notes</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['description'] = meta['description'] + temp['desc'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Year</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ year }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['year'] = temp['year'] 
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
        <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em>Publication</em></font></th>

    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ publication }}</font>
    </td>
        *}
        """,
        url=urlz)
    try:        
        meta['publication'] = temp['publication']
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
    temp = scrapemark.scrape("""
        {*
    <th align="left" valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;" face="Verdana"><em>Date Completed</em></font></th>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ date }}</font>
        *}
        """,
        url=urlz)
    try:
        inventory['date'] = temp['date']
    except NameError:
        meta['description'] = meta['description']
    except TypeError:
        meta['description'] = meta['description']
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

    functionalunit = 
    temp = scrapemark.scrape("""
        {*
<td valign="top" width="257" bgcolor="#DCDEE0"><font style="font-size: 11px;"><em><a name="Functional Unit"><strong>Functional Unit</strong></a><br>
    (see also <a href="#Functional Unit Explanation">Functional Unit
    Explanation</a>)</em></font></font></td>
    <td valign="top" width="477" bgcolor="#FFFFFF"><font style="font-size: 11px;">{{ desc }}</font>
    </td>
        *}
        """,
        url=urlz)
    functionalunit = temp['desc']
    fulluri = 'http://footprinted.org/rdfspace/lca/' + name
    lcistr = '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:eco="http://ontology.earthster.org/eco/core#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"><rdf:Description rdf:about="http://footprinted.org/rdfspace/lca/' + name + '"><rdfs:type rdf:resource="http://ontology.earthster.org/eco/core#LCAModel"/>'
    lcistr = lcistr + '<rdfs:label rdf:resource="' + name + '"/>'      
    lcistr = lcistr + '<eco:models rdf:nodeID="process' + urlz + '"/>' 
    lcistr = lcistr + getIO(name, urlz)
    lcistr = lcistr +  "</rdf:Description></rdf:RDF>"
    scraperwiki.sqlite.execute("insert into SPINE values (?,?,?)", (urlz, fulluri,lcistr))
    scraperwiki.sqlite.commit() 
    #publication
    num = "1";
    biburi = "http://footprinted.org/rdfspace/bibliography/" + num
    bibrdf = "<rdf:RDF><rdf:Description><rdf:about>http://footprinted.org/rdfspace/bibliography/" + num + "</rdf:about><dc:title>" + meta['publication'] + "</dc:title></rdf:Description></rdf:RDF>"
    scraperwiki.sqlite.execute("insert into SPINE values (?,?,?)", (urlz, biburi,bibrdf))
    scraperwiki.sqlite.commit() 

def getIO(name, urlz):
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
    inventorystr = ""
    for flow in ios['io']:
        if flow['direction'] == "Input" or flow['direction'] == "Output":
            inventorystr = inventorystr + "<eco:hasUnallocatedExchange>";
            inventorystr = inventorystr + '<eco:hasEffect><rdfs:type rdf:resource="eco:' + flow['direction'] + '" /><eco:hasTransferable><eco:Substance><rdfs:label>' + flow['substance'] + '</rdfs:label></eco:Substance></eco:hasTransferable></eco:hasEffect>'
            inventorystr = inventorystr + "<eco:hasQuantity><eco:hasUnitOfMeasure>" + flow["unit"] + "</eco:hasUnitOfMeasure><eco:hasMagnitude>" + flow["value"] + "</eco:hasMagnitude><ecoUD:maxValue>" + flow["max"] + "</ecoUD:maxValue><ecoUD:minValue>" + flow["min"] + "</ecoUD:minValue><ecoUD:maxValue>" + flow["max"] + "</ecoUD:maxValue><ecoUD:ecoUD:standardDeviation95>" + flow["std"] + "</ecoUS:ecoUD:standardDeviation95></eco:hasQuantity>";
            inventorystr = inventorystr + '</eco:hasUnallocatedExchange>';
    return inventorystr

# Main
# http://cpmdatabase.cpm.chalmers.se/Scripts/sheet.asp?ActId=KI-2010-06-23-129
try:           
    scraperwiki.sqlite.execute("select * from SPINE")
except scraperwiki.sqlite.SqliteError, e:
    scraperwiki.sqlite.execute("create table SPINE ('spineurl','uri','rdf')")      
#scraperwiki.utils.httpresponseheader( "Content-Type", "text/xml")
rooturl = "http://cpmdatabase.cpm.chalmers.se/Scripts/"         
html = scraperwiki.scrape("http://cpmdatabase.cpm.chalmers.se/Scripts/General.asp?QBase=Process")
soup = BeautifulSoup(html)
pages = soup.findAll(attrs={'href' : re.compile("sheet.asp\?ActId=*.")});
#testpage = "http://cpmdatabase.cpm.chalmers.se/Scripts/sheet.asp?ActId=ECOP3225"
x = 1;
for p in pages:
    fullurl = rooturl + p['href']
    getEachRecord(p.parent.parent.contents[3].text,fullurl.replace(" ", "%20"))
    x = x +1
    if x == 2:
        exit