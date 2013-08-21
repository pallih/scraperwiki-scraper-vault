import scraperwiki
import urllib
from lxml import etree
import time
from xml.etree.cElementTree import tostring
import mechanize
import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'unit' in get: unit=get['unit']
    else: unit=''
    if 'unitset' in get: unitset=get['unitset']
    else: unitset=''
    if 'keywordsearch' in get: keywordsearch=get['keywordsearch']
    else: keywordsearch=''
else:
    unit=''
    unitset=''
    keywordsearch=''

#unit='K311_4'
#unitset='T180'
#keywordsearch='physics'
#unit='T180_1'
def freemindRoot(title):
    mm=etree.Element("map")
    mm.set("version", "0.9.0")
    root=etree.SubElement(mm,"node")
    root.set("CREATED",str(int(time.time())))
    root.set("STYLE","fork")
    root.set("TEXT",title)   
    return mm,root

def unitGrab(ccurl):
    br = mechanize.Browser()
    brc=br.open(ccurl)
    tree = etree.parse(brc)
    courseRoot = tree.getroot()
    return courseRoot

def freemindRoot2(ccurl):
    br = mechanize.Browser()
    brc=br.open(ccurl)
    tree = etree.parse(brc)
    courseRoot = tree.getroot()
    mm=etree.Element("map")
    mm.set("version", "0.9.0")
    root=etree.SubElement(mm,"node")
    root.set("CREATED",str(int(time.time())))
    root.set("STYLE","fork")
    #We probably need to bear in mind escaping the text strings?
    #courseRoot: The course title is not represented consistently in the T151 SA docs, so we need to flatten it
    title=flatten(courseRoot.find('CourseTitle'))
    root.set("TEXT",title)
    return mm,courseRoot,root

def freemindRoot3(keyword):
    mm=etree.Element("map")
    mm.set("version", "0.9.0")
    root=etree.SubElement(mm,"node")
    root.set("CREATED",str(int(time.time())))
    root.set("STYLE","fork")
    root.set("TEXT",keyword)
    return mm, root
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

def learningOutcomes(courseRoot,root):
    los=courseRoot.findall('.//Unit/LearningOutcomes/LearningOutcome')
    if len(los)==0: los=courseRoot.findall('.//FrontMatter/LearningOutcomes/LearningOutcome')
    if len(los)==0: return
    mmlos=etree.SubElement(root,"node")
    mmlos.set("TEXT","Learning Outcomes")
    mmlos.set("FOLDED","true")

    for lo in los:
        mmsession=etree.SubElement(mmlos,"node")
        mmsession.set("TEXT",flatten(lo))

def parsePage(courseRoot,root):
    unitTitle=courseRoot.find('.//ItemTitle')

    mmweek=etree.SubElement(root,"node")
    mmweek.set("TEXT",flatten(unitTitle))
    mmweek.set("FOLDED","true")

    learningOutcomes(courseRoot,mmweek)
    
    sessions=courseRoot.findall('.//Session')
    for session in sessions:
        title=flatten(session.find('.//Title'))
        if title=='':continue
        #print 's',title
        mmsession=etree.SubElement(mmweek,"node")
        mmsession.set("TEXT",title)
        mmsession.set("FOLDED","true")
        subsessions=session.findall('.//Section')
        for subsession in subsessions:
            heading=subsession.find('.//Title')
            if heading !=None:
                title=flatten(heading)
                #print 'ss',title
                if title.strip()!='':
                    mmsubsession=etree.SubElement(mmsession,"node")
                    mmsubsession.set("TEXT",title)
                    mmsubsession.set("FOLDED","true")

def unitsmapper(data):
    for row in data:
        #G.add_node(row['unitcode'],label=row['unitcode'],name=row['name'],parentCC=row['parentCourseCode'])
        if row['ccu'] not in lounits: continue
        topic=row['topic']
        if topic not in topics:
            topics.append(topic)
            mmtopics[topic]=etree.SubElement(root,"node")
            mmtopics[topic].set("TEXT",topic)
            mmtopics[topic].set("FOLDED","true")
    
        parentCourseCode=row['cc']
        if parentCourseCode not in parentCourses:
            parentCourses.append(parentCourseCode)
            mmpcourses[parentCourseCode]=etree.SubElement(mmtopics[topic],"node")
            mmpcourses[parentCourseCode].set("TEXT",parentCourseCode)
            mmpcourses[parentCourseCode].set("FOLDED","true")

        mmunit=row['ccu']
        if mmunit not in mmunits:
            units.append(mmunit)
            mmunits[mmunit]=etree.SubElement(mmpcourses[parentCourseCode],"node")
            mmunits[mmunit].set("TEXT",row['uname'])
            mmunits[mmunit].set("FOLDED","true")

    for row in lodata:
        node=mmunits[row['ccu']]
        lo=etree.SubElement(node,"node")
        lo.set("TEXT",row['lo'])
        lo.set("FOLDED","true")

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
#keywordsearch='physics'
if unit=='' and unitset=='' and keywordsearch=='':
    scraperwiki.sqlite.attach( 'openlearn_xml_processor' )
    q = '* FROM "unitsHome" order by ccu'
    data = scraperwiki.sqlite.select(q)

    q = '* FROM "learningoutcomes"'
    lodata = scraperwiki.sqlite.select(q)

    lounits=[]
    for row in lodata:
        if row['ccu'] not in lounits: lounits.append(row['ccu'])

    title="OpenLearn"
    mm,root=freemindRoot(title)

    topics=[]
    parentCourses=[]
    units=[]
    mmtopics={}
    mmpcourses={}
    mmunits={}

    unitsmapper(data)
    print tostring(mm)
elif unit!='':
    scraperwiki.sqlite.attach( 'openlearn_xml_processor' )
    q = '* FROM "unitsHome" where ccu = "'+unit+'"'
    data = scraperwiki.sqlite.select(q)
    url=data[0]['ccurl']+'&content=1'
    mm,courseRoot,root=freemindRoot2(url)
    parsePage(courseRoot,root)
    print tostring(mm)
elif unitset!='' :
    scraperwiki.sqlite.attach( 'openlearn_xml_processor' )
    q = '* FROM "unitsHome" where cc = "'+unitset+'" order by ccu'
    data = scraperwiki.sqlite.select(q)
    #print data
    url=data[0]['ccurl']+'&content=1'
    mm,courseRoot,root=freemindRoot2(url)
    for record in data:
        #print record
        url=record['ccurl']+'&content=1'
        unit=record['ccu']
        courseRoot=unitGrab(url)
        parsePage(courseRoot,root)
    print tostring(mm)
elif keywordsearch!='':
    scraperwiki.sqlite.attach( 'openlearn_xml_processor' )
    q = 'DISTINCT ccu,url FROM "quickkeywords" where keyword like "%'+keywordsearch+'%" order by ccu'
    data = scraperwiki.sqlite.select(q)
    #print data
    url=data[0]['url']+'&content=1'
    mm,root=freemindRoot3(keywordsearch)
    for record in data:
        #print record
        url=record['url']+'&content=1'
        unit=record['ccu']
        courseRoot=unitGrab(url)
        parsePage(courseRoot,root)
    print tostring(mm)
