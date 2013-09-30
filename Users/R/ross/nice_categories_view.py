from xml.dom.minidom import Document
from xml.sax.saxutils import unescape
import scraperwiki
    
class XmlWriter:

    def __init__(self):
        self.doc = Document()

    def createNode(self, nodeName, parentNode = '', withAttribs = {}):
        node = self.doc.createElement(nodeName)
        if parentNode == '':
            createdNode = self.doc.appendChild(node)
        else:               
            createdNode = parentNode.appendChild(node)

        if withAttribs != {}:
            for key, value in withAttribs.items():
                self.setAttribute(createdNode, key, value)
 
        return createdNode
 
    def setAttribute(self, node, key, value):
        node.setAttribute(key, value)
 
    def printXML(self):
        return self.doc.toprettyxml(indent="  ")


scraperwiki.utils.httpresponseheader("Content-Type","application/xml")

"""
data = 
{
   "": { "" : [] }
}
"""
doc = XmlWriter()
node  = doc.createNode('guidelines')
nodep = doc.createNode('provider', node, withAttribs = {'name': 'NICE'})

scraperwiki.sqlite.attach('nice_categorised')
resultset = scraperwiki.sqlite.execute('select distinct(category) from nice_categorised.data')
resultset = sum(resultset['data'], [])
d = dict([(k,{},) for k in resultset])
for c in resultset:
    r = sum(scraperwiki.sqlite.execute('select distinct(subcategory) from nice_categorised.data where category="%s"' % c)['data'],[])
    for sc in r:
        d[c][sc] = []

resultset = scraperwiki.sqlite.select('* from nice_categorised.data')
for record in resultset:
    d[record['category']][record['subcategory']].append( record )


for ktop in sorted(d.keys()):
    subdict = d[ktop]    
    nodec = doc.createNode('category', nodep, withAttribs={'name': ktop})
    for k in sorted(subdict.keys()):
        vlist = subdict[k]
        if k == '':
            node_add = nodec
        else:
            node_add = doc.createNode('category', nodec, withAttribs={'name': k})
            node_add.text = "xx"
        
        for record in sorted(vlist, key=lambda k: k['title']):
            u = record['url']
            t = record['title']
            del record['title']
            del record['url']
            nodeg = doc.createNode('guideline', node_add, withAttribs=record)
            nodeu = doc.createNode( 'url', nodeg )
            nodeu.appendChild( doc.doc.createTextNode( u ) )
            nodet = doc.createNode( 'title', nodeg )
            nodet.appendChild( doc.doc.createTextNode( t ) )

    
print doc.printXML()

from xml.dom.minidom import Document
from xml.sax.saxutils import unescape
import scraperwiki
    
class XmlWriter:

    def __init__(self):
        self.doc = Document()

    def createNode(self, nodeName, parentNode = '', withAttribs = {}):
        node = self.doc.createElement(nodeName)
        if parentNode == '':
            createdNode = self.doc.appendChild(node)
        else:               
            createdNode = parentNode.appendChild(node)

        if withAttribs != {}:
            for key, value in withAttribs.items():
                self.setAttribute(createdNode, key, value)
 
        return createdNode
 
    def setAttribute(self, node, key, value):
        node.setAttribute(key, value)
 
    def printXML(self):
        return self.doc.toprettyxml(indent="  ")


scraperwiki.utils.httpresponseheader("Content-Type","application/xml")

"""
data = 
{
   "": { "" : [] }
}
"""
doc = XmlWriter()
node  = doc.createNode('guidelines')
nodep = doc.createNode('provider', node, withAttribs = {'name': 'NICE'})

scraperwiki.sqlite.attach('nice_categorised')
resultset = scraperwiki.sqlite.execute('select distinct(category) from nice_categorised.data')
resultset = sum(resultset['data'], [])
d = dict([(k,{},) for k in resultset])
for c in resultset:
    r = sum(scraperwiki.sqlite.execute('select distinct(subcategory) from nice_categorised.data where category="%s"' % c)['data'],[])
    for sc in r:
        d[c][sc] = []

resultset = scraperwiki.sqlite.select('* from nice_categorised.data')
for record in resultset:
    d[record['category']][record['subcategory']].append( record )


for ktop in sorted(d.keys()):
    subdict = d[ktop]    
    nodec = doc.createNode('category', nodep, withAttribs={'name': ktop})
    for k in sorted(subdict.keys()):
        vlist = subdict[k]
        if k == '':
            node_add = nodec
        else:
            node_add = doc.createNode('category', nodec, withAttribs={'name': k})
            node_add.text = "xx"
        
        for record in sorted(vlist, key=lambda k: k['title']):
            u = record['url']
            t = record['title']
            del record['title']
            del record['url']
            nodeg = doc.createNode('guideline', node_add, withAttribs=record)
            nodeu = doc.createNode( 'url', nodeg )
            nodeu.appendChild( doc.doc.createTextNode( u ) )
            nodet = doc.createNode( 'title', nodeg )
            nodet.appendChild( doc.doc.createTextNode( t ) )

    
print doc.printXML()

from xml.dom.minidom import Document
from xml.sax.saxutils import unescape
import scraperwiki
    
class XmlWriter:

    def __init__(self):
        self.doc = Document()

    def createNode(self, nodeName, parentNode = '', withAttribs = {}):
        node = self.doc.createElement(nodeName)
        if parentNode == '':
            createdNode = self.doc.appendChild(node)
        else:               
            createdNode = parentNode.appendChild(node)

        if withAttribs != {}:
            for key, value in withAttribs.items():
                self.setAttribute(createdNode, key, value)
 
        return createdNode
 
    def setAttribute(self, node, key, value):
        node.setAttribute(key, value)
 
    def printXML(self):
        return self.doc.toprettyxml(indent="  ")


scraperwiki.utils.httpresponseheader("Content-Type","application/xml")

"""
data = 
{
   "": { "" : [] }
}
"""
doc = XmlWriter()
node  = doc.createNode('guidelines')
nodep = doc.createNode('provider', node, withAttribs = {'name': 'NICE'})

scraperwiki.sqlite.attach('nice_categorised')
resultset = scraperwiki.sqlite.execute('select distinct(category) from nice_categorised.data')
resultset = sum(resultset['data'], [])
d = dict([(k,{},) for k in resultset])
for c in resultset:
    r = sum(scraperwiki.sqlite.execute('select distinct(subcategory) from nice_categorised.data where category="%s"' % c)['data'],[])
    for sc in r:
        d[c][sc] = []

resultset = scraperwiki.sqlite.select('* from nice_categorised.data')
for record in resultset:
    d[record['category']][record['subcategory']].append( record )


for ktop in sorted(d.keys()):
    subdict = d[ktop]    
    nodec = doc.createNode('category', nodep, withAttribs={'name': ktop})
    for k in sorted(subdict.keys()):
        vlist = subdict[k]
        if k == '':
            node_add = nodec
        else:
            node_add = doc.createNode('category', nodec, withAttribs={'name': k})
            node_add.text = "xx"
        
        for record in sorted(vlist, key=lambda k: k['title']):
            u = record['url']
            t = record['title']
            del record['title']
            del record['url']
            nodeg = doc.createNode('guideline', node_add, withAttribs=record)
            nodeu = doc.createNode( 'url', nodeg )
            nodeu.appendChild( doc.doc.createTextNode( u ) )
            nodet = doc.createNode( 'title', nodeg )
            nodet.appendChild( doc.doc.createTextNode( t ) )

    
print doc.printXML()

from xml.dom.minidom import Document
from xml.sax.saxutils import unescape
import scraperwiki
    
class XmlWriter:

    def __init__(self):
        self.doc = Document()

    def createNode(self, nodeName, parentNode = '', withAttribs = {}):
        node = self.doc.createElement(nodeName)
        if parentNode == '':
            createdNode = self.doc.appendChild(node)
        else:               
            createdNode = parentNode.appendChild(node)

        if withAttribs != {}:
            for key, value in withAttribs.items():
                self.setAttribute(createdNode, key, value)
 
        return createdNode
 
    def setAttribute(self, node, key, value):
        node.setAttribute(key, value)
 
    def printXML(self):
        return self.doc.toprettyxml(indent="  ")


scraperwiki.utils.httpresponseheader("Content-Type","application/xml")

"""
data = 
{
   "": { "" : [] }
}
"""
doc = XmlWriter()
node  = doc.createNode('guidelines')
nodep = doc.createNode('provider', node, withAttribs = {'name': 'NICE'})

scraperwiki.sqlite.attach('nice_categorised')
resultset = scraperwiki.sqlite.execute('select distinct(category) from nice_categorised.data')
resultset = sum(resultset['data'], [])
d = dict([(k,{},) for k in resultset])
for c in resultset:
    r = sum(scraperwiki.sqlite.execute('select distinct(subcategory) from nice_categorised.data where category="%s"' % c)['data'],[])
    for sc in r:
        d[c][sc] = []

resultset = scraperwiki.sqlite.select('* from nice_categorised.data')
for record in resultset:
    d[record['category']][record['subcategory']].append( record )


for ktop in sorted(d.keys()):
    subdict = d[ktop]    
    nodec = doc.createNode('category', nodep, withAttribs={'name': ktop})
    for k in sorted(subdict.keys()):
        vlist = subdict[k]
        if k == '':
            node_add = nodec
        else:
            node_add = doc.createNode('category', nodec, withAttribs={'name': k})
            node_add.text = "xx"
        
        for record in sorted(vlist, key=lambda k: k['title']):
            u = record['url']
            t = record['title']
            del record['title']
            del record['url']
            nodeg = doc.createNode('guideline', node_add, withAttribs=record)
            nodeu = doc.createNode( 'url', nodeg )
            nodeu.appendChild( doc.doc.createTextNode( u ) )
            nodet = doc.createNode( 'title', nodeg )
            nodet.appendChild( doc.doc.createTextNode( t ) )

    
print doc.printXML()

