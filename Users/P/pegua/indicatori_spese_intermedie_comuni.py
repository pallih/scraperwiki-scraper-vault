import scraperwiki
import urllib2
import lxml.etree

url = "http://ph34r.altervista.org/spese-citta.pdf"

pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

left_index=[]
left_index.append({'cancelleria':[176,328],'comunicazione':[486,637],'equipaggiamenti':[795,947],'trasporto_pubblico':[1105,1256],'rifiuti':[1414,1566]})
left_index.append({'incarichi':[174,326],'manutenzione':[484,635],'pulizia':[793,945],'utente':[1103,1254],'affitti_noleggi':[1412,1564]})

for index_pag in range(len(pages)):
    tags = list(pages[index_pag])
    for index_tag in range(len(tags)):
        v = tags[index_tag]
        if v.tag == 'fontspec':
            continue
        assert v.tag == 'text'
        for key in left_index[index_pag].iterkeys():
            #print key
            #print v.get('left')
            #print left_index[index_pag][key]
            
            if( int(v.get('left')) in left_index[index_pag][key]):
                l = list(tags[index_tag+1])
                t = l[0]
                record = {}
                record["CategoriaSpese"] = key
                record["NomeEnte"] = "Comune di " + v.text
                record["Spesa"] = (t.text).replace(".","")
                scraperwiki.sqlite.save(unique_keys=["CategoriaSpese","NomeEnte"], data=record)  
                


import scraperwiki
import urllib2
import lxml.etree

url = "http://ph34r.altervista.org/spese-citta.pdf"

pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

left_index=[]
left_index.append({'cancelleria':[176,328],'comunicazione':[486,637],'equipaggiamenti':[795,947],'trasporto_pubblico':[1105,1256],'rifiuti':[1414,1566]})
left_index.append({'incarichi':[174,326],'manutenzione':[484,635],'pulizia':[793,945],'utente':[1103,1254],'affitti_noleggi':[1412,1564]})

for index_pag in range(len(pages)):
    tags = list(pages[index_pag])
    for index_tag in range(len(tags)):
        v = tags[index_tag]
        if v.tag == 'fontspec':
            continue
        assert v.tag == 'text'
        for key in left_index[index_pag].iterkeys():
            #print key
            #print v.get('left')
            #print left_index[index_pag][key]
            
            if( int(v.get('left')) in left_index[index_pag][key]):
                l = list(tags[index_tag+1])
                t = l[0]
                record = {}
                record["CategoriaSpese"] = key
                record["NomeEnte"] = "Comune di " + v.text
                record["Spesa"] = (t.text).replace(".","")
                scraperwiki.sqlite.save(unique_keys=["CategoriaSpese","NomeEnte"], data=record)  
                


