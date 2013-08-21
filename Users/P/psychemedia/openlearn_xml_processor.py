import scraperwiki
import mechanize

from lxml import etree

debug=False
# http://openlearn.open.ac.uk/rss/file.php/stdfeed/1/full_opml.xml

phase=1

#===
#via http://stackoverflow.com/questions/5757201/help-or-advice-me-get-started-with-lxml/5899005#5899005
def flatten(el):           
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)
#===

def handleTopic(topicRoot):
    #Need to get URL, load in page, find URL for actual unit, generate XML URL, parse and handle XML
    pass

def getcontenturl(srcUrl):
    print srcUrl
    #br = mechanize.Browser()
    #brc=br.open(srcUrl)
    rss= etree.parse(srcUrl)
    rssroot=rss.getroot()
    xid=''
    contenturl= flatten(rssroot.find('./channel/item/link'))
    courseCode=flatten(rssroot.find('.//{http://purl.org/dc/elements/1.1/}identifier'))
        
    rssitems=rssroot.findall('.//item')
    for item in rssitems:
        if debug: print 'trying...'
        itemlink=flatten(item.find('.//link'))
        contexttitle=flatten(item.find('.//title'))
        assets=item.findall('.//{http://search.yahoo.com/mrss/}content')
        for asset in assets:
            url=asset.get('url')
            filesize=asset.get('filesize')
            atype=asset.get('type')
            xid=url.split('/!via/oucontent/course/')
            #http://openlearn.open.ac.uk/file.php/1632/!via/oucontent/course/31/a103_3_001i.jpg
            if debug: print 'xid',xid,xid[1]
            x2id=xid[0].split('/')[-1]
            fsuffix=xid[1].split('.')[-1]
            fname=xid[1].split('/')[-1]
            xid=xid[1].split('/')[0]
            
            if debug: print url,filesize,atype,xid,x2id,fsuffix,fname
            scraperwiki.sqlite.save(unique_keys=['kkey'], table_name='quickassets', data={'kkey':courseCode+'_'+fname,'ccu':courseCode,'url':url,'filesize':filesize,'atype':atype,'itemlink':itemlink,'contexttitle':contexttitle,'xid':xid,'x2id':x2id,'fsuffix':fsuffix,'fname':fname})
        firstitem=rssroot.find('./channel/item')
    keywords=firstitem.findall('.//{http://purl.org/dc/elements/1.1/}subject')
    for keyword in keywords:
        if debug: print flatten(keyword)
        scraperwiki.sqlite.save(unique_keys=[],table_name='quickkeywords',data={'ccu':courseCode,'url':contenturl,'keyword':flatten(keyword)})
    return contenturl,xid

def getUnitLocations():
    #The OPML file lists all OpenLearn units by topic area
    srcUrl='http://openlearn.open.ac.uk/rss/file.php/stdfeed/1/full_opml.xml'
    tree = etree.parse(srcUrl)
    root = tree.getroot()
    topics=root.findall('.//body/outline')
    units=[]
    #Handle each topic area separately?
    for topic in topics:
        tt = topic.get('text')
        if debug: print tt
        for item in topic.findall('./outline'):
            it=item.get('text')
            if it.startswith('Unit content for'):
                it=it.replace('Unit content for','')
                url=item.get('htmlUrl')
                rssurl=item.get('xmlUrl')
                ccu=url.split('=')[1]
                cctmp=ccu.split('_')
                cc=cctmp[0]
                if len(cctmp)>1: ccpart=cctmp[1]
                else: ccpart=1
                slug=rssurl.replace('http://openlearn.open.ac.uk/rss/file.php/stdfeed/','')
                slug=slug.split('/')[0]
                contenturl,xid=getcontenturl(rssurl)
                ccid=contenturl
                ccid=ccid.split('=')
                ccid=ccid[1]
                if debug: print tt,it,slug,ccu,cc,ccpart,url,contenturl,ccid
                scraperwiki.sqlite.save(unique_keys=['ccu'], table_name='unitsHome', data={'ccu':ccu, 'uname':it,'topic':tt,'slug':slug,'cc':cc,'ccpart':ccpart,'url':url,'rssurl':rssurl,'ccurl':contenturl,'ccid':ccid,'xid':xid})
                units.append(ccu)
    return units

def parseGlossary(courseRoot,courseCode,courseID):
    #courseCode=flatten(courseRoot.find('.//CourseCode'))
    glossary=courseRoot.findall('.//BackMatter/Glossary/GlossaryItem')
    print courseCode, len(glossary),'glossary items'
    for glossitem in glossary:
        term=flatten(glossitem.find('Term'))
        term=term.strip()
        term=term.strip(':')
        term=term.split()
        term[0]=term[0].capitalize()
        term=' '.join(term)
        definition=flatten(glossitem.find('Definition'))
        if term!='':
            if debug: print courseCode,term,definition
            scraperwiki.sqlite.save(unique_keys=[],table_name='glossary',data={'ccu':courseCode,'term':term,'definition':definition,'ccid':courseID})
        #fudge the output for now to ignore non-ascii characters
        #writer.writerow([courseCode.encode('ascii','ignore'),term.encode('ascii','ignore'),definition.encode('ascii','ignore')])

def learningOutcomes(courseRoot,courseCode):
    #courseCode=flatten(courseRoot.find('.//CourseCode'))
    los=courseRoot.findall('.//FrontMatter/LearningOutcomes/LearningOutcome')
    if len(los)==0: los=courseRoot.findall('.//Unit/LearningOutcomes/LearningOutcome')
    print courseCode, len(los),'LOs'
    for lo in los:
        scraperwiki.sqlite.save(unique_keys=[],table_name='learningoutcomes',data={'ccu':courseCode,'lo':flatten(lo)})


def mediaAssets(courseRoot,courseCode,courseID,xID,slug):
    assets=courseRoot.findall('.//MediaContent')
    for asset in assets:
        msrc=asset.get('src')
        mtyp=asset.get('type')
        mid=asset.get('id')
        if debug: print 'mediaassets',mtyp,mid,msrc
        scraperwiki.sqlite.save(unique_keys=[],table_name='mediaAssets',data={'ccu':courseCode,'src':msrc,'typ':mtyp,'id':mid,'ccid':courseID,'xid':xID,'slug':slug})


def figures(courseRoot,courseCode,courseID,xID,slug):
    #courseCode=flatten(courseRoot.find('.//CourseCode'))
    figures=courseRoot.findall('.//Figure')
    #Note that acknowledgements to figures are provided at the end of the XML file with only informal free text/figure number identifers available for associating a particular acknowledgement/copyright assignment with a given image. It would be so much neater if this could be bundled up with the figure itself, or if the figure and the acknowledgement could share the same unique identifier?
    for figure in figures:
        img=figure.find('Image')
        #Is there a way I can actually generate a behind the firewall at least URL for embedding actual images?
        src=img.get('src')
        xsrc=img.get('x_imagesrc')
        caption=flatten(figure.find('Caption'))
        #in desc, need to find a way of stripping <Number> element from start of description
        desc=flatten(figure.find('Description'))
        if debug: print 'figures',xsrc,caption,desc
        scraperwiki.sqlite.save(unique_keys=[],table_name='figures',data={'ccu':courseCode,'src':src,'xsrc':xsrc,'caption':caption,'desc':desc,'ccid':courseID,'xid':xID,'slug':slug})


def getUnit(unit):
    br = mechanize.Browser()
    cr=unit['ccurl']+'&content=1'
    ccid=unit['ccid']
    xid=unit['xid']
    slug=unit['slug']
    print cr,ccid

    try:
        brc=br.open(cr)
        tree = etree.parse(brc)
        root=tree.getroot()
        try:
            parseGlossary(root,unit['ccu'],ccid)
            learningOutcomes(root,unit['ccu'])
            figures(root,unit['ccu'],ccid,xid,slug)
            mediaAssets(root,unit['ccu'],ccid,xid,slug)
            scraperwiki.sqlite.save(unique_keys=['url'],table_name='parsedUnits',data={'ccu':unit['ccu'], 'url':unit['ccurl']})
        except:
            pass
    except:
        scraperwiki.sqlite.save(unique_keys=['ccu'],table_name='xmlerror',data={'ccu':unit['ccu'],'ccurl':unit['ccurl'], 'ccid':ccid})
        if debug: print 'err, oops...?',brc.read()

def getUnits():
    units= scraperwiki.sqlite.select("* from `unitsHome`")
    try:
        parsedUnits=scraperwiki.sqlite.select("* from `parsedUnits`")
    except: parsedUnits=[]
    pUnits=[]
    for punit in parsedUnits: pUnits.append(punit['ccu'])
    for unit in units:
        if unit['ccu'] not in pUnits:
            getUnit(unit)

def droptable(table):
    try:
        scraperwiki.sqlite.execute('drop table "'+table+'"')
    except:
        pass

#scraperwiki.sqlite.execute('drop table "glossary"')
#scraperwiki.sqlite.execute('drop table "figures"')
#scraperwiki.sqlite.execute('drop table "learningoutcomes"')
#scraperwiki.sqlite.execute('drop table "xmlerror"')
if phase==0:
    droptable("unitsHome")
    droptable('quickassets')
    droptable('quickkeywords')
    getUnitLocations()
elif phase==1:
    getUnitLocations()
    getUnits()
elif phase==2:
    getUnits()
elif phase==3:
    droptable("glossary")
    droptable("figures")
    droptable("learningoutcomes")
    droptable("xmlerror")
    droptable('mediaAssets')
    droptable("parsedUnits")
    getUnits()
elif phase==4:
    droptable("unitsHome")
    droptable('quickassets')
    droptable('quickkeywords')
    getUnitLocations()
    droptable("glossary")
    droptable("figures")
    droptable("learningoutcomes")
    droptable("xmlerror")
    droptable('mediaAssets')
    droptable("parsedUnits")
    getUnits()
#getUnitLocations()
#need to check that if unit has already been scraped; if so, ignore it
#getUnits()
