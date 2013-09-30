import scraperwiki
import urllib
from lxml import etree
import time
from xml.etree.cElementTree import tostring
import mechanize
import cgi, os
import networkx as nx


qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'unit' in get: unit=get['unit']
    elif 'unitset' in get:
        unitset=get['unitset']
        unit=''
    else: unit='A224_1'
else:
    unit='A224_1'


#TO DO
#--rewrite using networkx rather than lxml
#--export as json http://networkx.lanl.gov/reference/generated/networkx.readwrite.json_graph.tree_data.html

#===
#via http://stackoverflow.com/questions/5757201/help-or-advice-me-get-started-with-lxml/5899005#5899005
def flatten(el):
    if el==None:return ''
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)
#===

def simpleRoot(DG,title,currRoot):
    DG.add_node(currRoot,name=ascii(title))
    return DG

def graphMMRoot(DG,ccurl,currRoot=1,currNode=-1):
#def freemindRoot2(ccurl):
    br = mechanize.Browser()
    brc=br.open(ccurl)
    tree = etree.parse(brc)
    courseRoot = tree.getroot()
    #mm=etree.Element("map")
    #mm.set("version", "0.9.0")
    ##root=etree.SubElement(mm,"node")
    #root.set("CREATED",str(int(time.time())))
    #root.set("STYLE","fork")
    #We probably need to bear in mind escaping the text strings?
    #courseRoot: The course title is not represented consistently in the T151 SA docs, so we need to flatten it
    if currNode==-1:title=flatten(courseRoot.find('CourseTitle'))
    else: title=flatten(courseRoot.find('ItemTitle'))
    #root.set("TEXT",title)
    if currNode==-1:
        DG.add_node(currRoot,name=ascii(title))
        currNode=currRoot
    else: DG,currNode=gNodeAdd(DG,currRoot,currNode,title)
    #return mm,courseRoot,root
    #print '9',currNode
    return DG,courseRoot,currNode,currRoot

def gNodeAdd(DG,root,node,name):
    node=node+1
    #print str(root),'..',str(node)
    DG.add_node(node,name=ascii(name))
    DG.add_edge(root,node)
    return DG,node

def learningOutcomes(courseRoot,DG,currRoot,currCount=-1):
    if currCount==-1: currCount=currRoot
    los=courseRoot.findall('.//Unit/LearningOutcomes/LearningOutcome')
    if len(los)==0: los=courseRoot.findall('.//FrontMatter/LearningOutcomes/LearningOutcome')
    if len(los)==0: return
    #mmlos=etree.SubElement(root,"node")
    #mmlos.set("TEXT","Learning Outcomes")
    #mmlos.set("FOLDED","true")

    #nc=currRoot+1
    #DG.add_node(nc,name="Learning Outcomes")
    #DG.add_edge(currRoot,nc)
    DG,nc=gNodeAdd(DG,currRoot,currCount,"Learning Outcomes")
    #print '5',nc
    currRoot=nc
    for lo in los:
        #mmsession=etree.SubElement(mmlos,"node")
        #mmsession.set("TEXT",flatten(lo))
        #nc=nc+1
        #DG.add_node(nc,name=ascii(flatten(lo)))
        #DG.add_edge(currRoot,nc)
        DG,nc=gNodeAdd(DG,currRoot,nc,flatten(lo))
        #print '6',nc
    return DG,nc

#def parsePage(courseRoot,root):
def graphParsePage(courseRoot,DG,currRoot,currCount=-1):
    if currCount==-1: currCount=currRoot
    unitTitle=courseRoot.find('.//ItemTitle')

    #mmweek=etree.SubElement(root,"node")
    #mmweek.set("TEXT",flatten(unitTitle))
    #mmweek.set("FOLDED","true")

    #nc=currRoot+1
    #DG.add_node(nc,name=ascii(flatten(unitTitle)))
    #DG.add_edge(currRoot,nc)
    DG,nc=gNodeAdd(DG,currRoot,currCount,flatten(unitTitle))
    #print '4',nc
    DG,nc=learningOutcomes(courseRoot,DG,currRoot,nc)
    #print '3',nc

    sessions=courseRoot.findall('.//Session')
    #print sessions
    for session in sessions:
        title=flatten(session.find('.//Title'))
        #print tostring(session)
        if title=='':continue
        #print 's',title
        #mmsession=etree.SubElement(mmweek,"node")
        #mmsession.set("TEXT",title)
        #mmsession.set("FOLDED","true")

        #nc=nc+1
        #DG.add_node(nc,name=ascii(title))
        #DG.add_edge(currRoot,nc)
        DG,nc=gNodeAdd(DG,currRoot,nc,title)
        #print '2',nc
        sessionRoot=nc

        subsessions=session.findall('.//Section')
        for subsession in subsessions:
            heading=subsession.find('.//Title')
            if heading !=None:
                title=flatten(heading)
                #print 'ss',title
                if title.strip()!='':
                    #mmsubsession=etree.SubElement(mmsession,"node")
                    #mmsubsession.set("TEXT",title)
                    #mmsubsession.set("FOLDED","true")
                    #nc=nc+1
                    #DG.add_node(nc,name=ascii(title))
                    #DG.add_edge(sessionRoot,nc)
                    DG,nc=gNodeAdd(DG,sessionRoot,nc,title)
                    #print '1',nc
    return DG,nc

from networkx.readwrite import json_graph
import json

def ascii(s): return "".join(i for i in s if ord(i)<128)

def unitGrab(ccurl):
    br = mechanize.Browser()
    brc=br.open(ccurl)
    tree = etree.parse(brc)
    courseRoot = tree.getroot()
    return courseRoot

currnode=1
scraperwiki.sqlite.attach( 'openlearn_xml_processor' )
DG=nx.DiGraph()
if unit!='':    
    q = '* FROM "unitsHome" where ccu = "'+unit+'"'
    data = scraperwiki.sqlite.select(q)
    #print data
    url=data[0]['ccurl']+'&content=1'
    DG,courseRoot,currnode,tmp=graphMMRoot(DG,url)
    #mm,courseRoot,root=freemindRoot2(url)
    #parsePage(courseRoot,root)
    #print tostring(mm)
    DG,currnode=graphParsePage(courseRoot,DG,currnode)
elif unitset!='':
    q = '* FROM "unitsHome" where cc = "'+unitset+'" order by ccu'
    data = scraperwiki.sqlite.select(q)
    #print data
    #url=data[0]['ccurl']+'&content=1'
    DG=simpleRoot(DG,unitset,1)
    #mm,courseRoot,root=freemindRoot2(url)
    for record in data:
        #print record
        url=record['ccurl']+'&content=1'
        DG,courseRoot,currnode,rootnode=graphMMRoot(DG,url,1,currnode)
        #unit=record['ccu']
        #courseRoot=unitGrab(url)
        #parsePage(courseRoot,root)
        #print ';;',rootnode,currnode
        DG,currnode=graphParsePage(courseRoot,DG,currnode)
        #print '7',currnode


scraperwiki.utils.httpresponseheader("Content-Type", "text/json")

data = json_graph.tree_data(DG,root=1)
print json.dumps(data)import scraperwiki
import urllib
from lxml import etree
import time
from xml.etree.cElementTree import tostring
import mechanize
import cgi, os
import networkx as nx


qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'unit' in get: unit=get['unit']
    elif 'unitset' in get:
        unitset=get['unitset']
        unit=''
    else: unit='A224_1'
else:
    unit='A224_1'


#TO DO
#--rewrite using networkx rather than lxml
#--export as json http://networkx.lanl.gov/reference/generated/networkx.readwrite.json_graph.tree_data.html

#===
#via http://stackoverflow.com/questions/5757201/help-or-advice-me-get-started-with-lxml/5899005#5899005
def flatten(el):
    if el==None:return ''
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)
#===

def simpleRoot(DG,title,currRoot):
    DG.add_node(currRoot,name=ascii(title))
    return DG

def graphMMRoot(DG,ccurl,currRoot=1,currNode=-1):
#def freemindRoot2(ccurl):
    br = mechanize.Browser()
    brc=br.open(ccurl)
    tree = etree.parse(brc)
    courseRoot = tree.getroot()
    #mm=etree.Element("map")
    #mm.set("version", "0.9.0")
    ##root=etree.SubElement(mm,"node")
    #root.set("CREATED",str(int(time.time())))
    #root.set("STYLE","fork")
    #We probably need to bear in mind escaping the text strings?
    #courseRoot: The course title is not represented consistently in the T151 SA docs, so we need to flatten it
    if currNode==-1:title=flatten(courseRoot.find('CourseTitle'))
    else: title=flatten(courseRoot.find('ItemTitle'))
    #root.set("TEXT",title)
    if currNode==-1:
        DG.add_node(currRoot,name=ascii(title))
        currNode=currRoot
    else: DG,currNode=gNodeAdd(DG,currRoot,currNode,title)
    #return mm,courseRoot,root
    #print '9',currNode
    return DG,courseRoot,currNode,currRoot

def gNodeAdd(DG,root,node,name):
    node=node+1
    #print str(root),'..',str(node)
    DG.add_node(node,name=ascii(name))
    DG.add_edge(root,node)
    return DG,node

def learningOutcomes(courseRoot,DG,currRoot,currCount=-1):
    if currCount==-1: currCount=currRoot
    los=courseRoot.findall('.//Unit/LearningOutcomes/LearningOutcome')
    if len(los)==0: los=courseRoot.findall('.//FrontMatter/LearningOutcomes/LearningOutcome')
    if len(los)==0: return
    #mmlos=etree.SubElement(root,"node")
    #mmlos.set("TEXT","Learning Outcomes")
    #mmlos.set("FOLDED","true")

    #nc=currRoot+1
    #DG.add_node(nc,name="Learning Outcomes")
    #DG.add_edge(currRoot,nc)
    DG,nc=gNodeAdd(DG,currRoot,currCount,"Learning Outcomes")
    #print '5',nc
    currRoot=nc
    for lo in los:
        #mmsession=etree.SubElement(mmlos,"node")
        #mmsession.set("TEXT",flatten(lo))
        #nc=nc+1
        #DG.add_node(nc,name=ascii(flatten(lo)))
        #DG.add_edge(currRoot,nc)
        DG,nc=gNodeAdd(DG,currRoot,nc,flatten(lo))
        #print '6',nc
    return DG,nc

#def parsePage(courseRoot,root):
def graphParsePage(courseRoot,DG,currRoot,currCount=-1):
    if currCount==-1: currCount=currRoot
    unitTitle=courseRoot.find('.//ItemTitle')

    #mmweek=etree.SubElement(root,"node")
    #mmweek.set("TEXT",flatten(unitTitle))
    #mmweek.set("FOLDED","true")

    #nc=currRoot+1
    #DG.add_node(nc,name=ascii(flatten(unitTitle)))
    #DG.add_edge(currRoot,nc)
    DG,nc=gNodeAdd(DG,currRoot,currCount,flatten(unitTitle))
    #print '4',nc
    DG,nc=learningOutcomes(courseRoot,DG,currRoot,nc)
    #print '3',nc

    sessions=courseRoot.findall('.//Session')
    #print sessions
    for session in sessions:
        title=flatten(session.find('.//Title'))
        #print tostring(session)
        if title=='':continue
        #print 's',title
        #mmsession=etree.SubElement(mmweek,"node")
        #mmsession.set("TEXT",title)
        #mmsession.set("FOLDED","true")

        #nc=nc+1
        #DG.add_node(nc,name=ascii(title))
        #DG.add_edge(currRoot,nc)
        DG,nc=gNodeAdd(DG,currRoot,nc,title)
        #print '2',nc
        sessionRoot=nc

        subsessions=session.findall('.//Section')
        for subsession in subsessions:
            heading=subsession.find('.//Title')
            if heading !=None:
                title=flatten(heading)
                #print 'ss',title
                if title.strip()!='':
                    #mmsubsession=etree.SubElement(mmsession,"node")
                    #mmsubsession.set("TEXT",title)
                    #mmsubsession.set("FOLDED","true")
                    #nc=nc+1
                    #DG.add_node(nc,name=ascii(title))
                    #DG.add_edge(sessionRoot,nc)
                    DG,nc=gNodeAdd(DG,sessionRoot,nc,title)
                    #print '1',nc
    return DG,nc

from networkx.readwrite import json_graph
import json

def ascii(s): return "".join(i for i in s if ord(i)<128)

def unitGrab(ccurl):
    br = mechanize.Browser()
    brc=br.open(ccurl)
    tree = etree.parse(brc)
    courseRoot = tree.getroot()
    return courseRoot

currnode=1
scraperwiki.sqlite.attach( 'openlearn_xml_processor' )
DG=nx.DiGraph()
if unit!='':    
    q = '* FROM "unitsHome" where ccu = "'+unit+'"'
    data = scraperwiki.sqlite.select(q)
    #print data
    url=data[0]['ccurl']+'&content=1'
    DG,courseRoot,currnode,tmp=graphMMRoot(DG,url)
    #mm,courseRoot,root=freemindRoot2(url)
    #parsePage(courseRoot,root)
    #print tostring(mm)
    DG,currnode=graphParsePage(courseRoot,DG,currnode)
elif unitset!='':
    q = '* FROM "unitsHome" where cc = "'+unitset+'" order by ccu'
    data = scraperwiki.sqlite.select(q)
    #print data
    #url=data[0]['ccurl']+'&content=1'
    DG=simpleRoot(DG,unitset,1)
    #mm,courseRoot,root=freemindRoot2(url)
    for record in data:
        #print record
        url=record['ccurl']+'&content=1'
        DG,courseRoot,currnode,rootnode=graphMMRoot(DG,url,1,currnode)
        #unit=record['ccu']
        #courseRoot=unitGrab(url)
        #parsePage(courseRoot,root)
        #print ';;',rootnode,currnode
        DG,currnode=graphParsePage(courseRoot,DG,currnode)
        #print '7',currnode


scraperwiki.utils.httpresponseheader("Content-Type", "text/json")

data = json_graph.tree_data(DG,root=1)
print json.dumps(data)