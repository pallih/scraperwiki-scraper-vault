##Trying out the unzip method found here:
#https://scraperwiki.com/scrapers/un_peacekeeping_statistics/
import tempfile, zipfile, urllib

#Rest of the script based on http://blog.ouseful.info/2012/05/03/sketching-partner-sponsors-of-uk-clinical-trials/

from lxml import etree
import networkx as nx
import networkx.readwrite.gexf as gf
from xml.etree.cElementTree import tostring
import scraperwiki

def flatten(el):
    if el != None:
        result = [ (el.text or "") ]
        for sel in el:
            result.append(flatten(sel))
            result.append(sel.tail or "")
        return "".join(result)
    return ''

def graphOut(DG):
    writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
    writer.add_graph(DG)
    print tostring(writer.xml)
    #f = open('workfile.gexf', 'w')
    #f.write(tostring(writer.xml))

def sponsorGrapher(DG,xmlRoot,sponsorList):
    sponsors_xml=xmlRoot.find('.//sponsors')
    lead=flatten(sponsors_xml.find('./lead_sponsor/agency'))
    if lead !='':
        if lead not in sponsorList:
            sponsorList.append(lead)
            DG.add_node(sponsorList.index(lead),label=lead,name=lead)
            
    for collab in sponsors_xml.findall('./collaborator/agency'):
        collabname=flatten(collab)
        if collabname !='':
            if collabname not in sponsorList:
                sponsorList.append(collabname)
                DG.add_node( sponsorList.index( collabname ), label=collabname, name=collabname, Label=collabname )
            DG.add_edge( sponsorList.index(lead), sponsorList.index(collabname) )
    return DG, sponsorList

def getXML(path,fn):
    fnp='/'.join([path,fn])
    xmldata=etree.parse(fnp)
    xmlRoot = xmldata.getroot()
    return xmlRoot

def parsePage(xmlRoot,sponsorGraph,sponsorList):
    sponsorGraph,sponsorList = sponsorGrapher(sponsorGraph,xmlRoot,sponsorList)
    return sponsorGraph,sponsorList

#XML_DATA_DIR='./ukClinicalTrialsData'
#listing = os.listdir(XML_DATA_DIR)
XML_ZIP='http://clinicaltrials.gov/ct2/results/download?down_stds=all&down_typ=study&down_flds=shown&down_fmt=plain&term=lung+cancer&show_flds=Y&show_down=Y'
#XML_ZIP='http://clinicaltrials.gov/ct2/results/download?down_stds=top100&down_typ=study&down_flds=shown&down_fmt=plain&cntry1=usa&show_flds=Y&show_down=Y'
#http://clinicaltrials.gov/ct2/results/download?down_stds=all&down_flds=all&down_fmt=tsv&term=fluoxetine
##FULL DOWNLOAD:
#http://clinicaltrials.gov/ct2/results/download?down_stds=all&down_typ=study&down_flds=shown&down_fmt=plain&cntry1=EU%3AGB&show_flds=Y&show_down=Y
#Australia PA%3AAU

#Full Australia data?
#XML_ZIP="http://clinicaltrials.gov/ct2/results/download?down_stds=all&down_typ=study&down_flds=shown&down_fmt=plain&cntry1=PA%3AAU&show_flds=Y&show_down=Y"


sponsorDG=nx.DiGraph()
sponsorList=[]


def getFiles(lurl,sponsorDG,sponsorList):
    t = tempfile.NamedTemporaryFile(suffix=".zip")
    t.write(urllib.urlopen(lurl).read())
    t.seek(0)
    z = zipfile.ZipFile(t.name)
    for nz in z.namelist():
    #    pdfbin = z.read(nz)
    #    ExtractPdf(year, nz, pdfbin, lurl)
        #print z.read(nz)
        xmls=z.read(nz)
        xmldata=etree.parse(StringIO.StringIO(xmls))
        #xmldata=etree.fromstring( xmls )
        #print xmldata
        xmlRoot=xmldata.getroot()
        sponsorDG, sponsorList = parsePage(xmlRoot, sponsorDG, sponsorList)
    return sponsorDG,sponsorList

import StringIO
scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")

sponsorDG,sponsorList = getFiles(XML_ZIP,sponsorDG,sponsorList)
'''
for page in listing:
    #if os.path.splitext( page )[1] =='.xml':
    #    sponsorDG, sponsorList = parsePage(XML_DATA_DIR,page, sponsorDG, sponsorList)
    #xmlRoot=getXML(path,fn)
    xmlRoot=z.read(page)
    sponsorDG, sponsorList = parsePage(xmlRoot, sponsorDG, sponsorList)
'''
graphOut(sponsorDG)