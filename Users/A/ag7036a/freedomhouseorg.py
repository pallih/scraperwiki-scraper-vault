import scraperwiki
import urllib2
import lxml.etree
from lxml.html import tostring, fromstring

def main():
    url="http://www.freedomhouse.org/sites/default/files/Freedom%20OnThe%20Net_Full%20Report.pdf"
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    
    goodpages=[27,28,29]

    rootdata=lxml.etree.fromstring(xmldata)
    pages = list(rootdata)

    page=pages[23]
    alltext=getText(page)
    dict1(alltext)
    for i in goodpages:
        page=pages[i]
        alltext=getText(page)
        dict2(alltext)
    
        pagenumbers=[30,36,47,53, 57, 61, 65, 72, 78, 82, 87, 97, 102, 108]
        Country=['Brazil', 'China', 'Cuba', 'Egypt', 'Estonia', 'Georgia', 'India', 'Iran', 'Kenya', 'Malaysia','Russia','Tunisia', 'Turkey', 'UK']
    for i in range(len(pagenumbers)):
        page=pages[pagenumbers[i]]
        alltext=getText(page)
        PageInfo(alltext, Country[i])
    

def getText(page):

    alltext=[]
    
    for node in page.findall("text"):
        bold=node.find("b") 
        if not bold is None:
            text2=bold.text
        else:
            text2=node.text
        top=node.attrib["top"]
        left = node.attrib["left"]
        if text2 != ' ' and text2 is not None and text2.strip()!='Africa':
            if text2.strip()== 'South':
                text2= 'South Africa'
                top='343'
            alltext.append([top, left, text2])
    return alltext


def dict1(alltext):
    D={}
    for data in alltext:
        if data[0] in D:
            row=D[data[0]]
            row.append(data)
            D[data[0]]=row
        else:
            D[data[0]]=[data]

    headers =['Country', 'Freedom Status', 'Freedom Total', 'A Subtota','B Subtotal', 'S Subtotal']
    for top in D:
        D2={} 
        l= D[top]
        if len(l)==6:
            for i in range (len(l)):
                D2[headers[i]]=str(l[i][2])
            scraperwiki.sqlite.save(['Country'],D2,table_name='freedom')

                


def dict2(alltext):
    D={}

    for data in alltext:
        if data[0] in D:
            row=D[data[0]]
            row.append(data)
            D[data[0]]=row
        else:
            D[data[0]]=[data]

    headers =['Country','b','c','Freedom of the Press Total', 'Freedom of the Press Status']
    for top in D:
        D2={}
        l= D[top]
        if len(l)==5:
            for i in [3,4]:
                D2[headers[i]]=l[i][2]
            D3=scraperwiki.sqlite.select("* from freedom where Country like '" + l[0][2].strip()+"%'")
            if len(D3)>0:
                D4=dict(D3[0].items()+D2.items())
                scraperwiki.sqlite.save(['Country'],D4,table_name='freedom')
                
            else:
                print 'Missing Country Name'+l[0][2]




def PageInfo(alltext, Country):
    D={}
    print alltext
    for data in alltext:
        if data[1] in D:
            row=D[data[1]]
            row.append(data)
            D[data[1]]=row
        else:
            D[data[1]]=[data]
    for left in D:
        l= D[left]
        if left=='445':
            for e in l:
                D2={}
                [key, data]=e[2].split(':')
                key=str(key).replace('/', '-').replace('(', '-').replace(')','-').replace('.','-')
                data=str(data)
                D2[key]=data
                D3=scraperwiki.sqlite.select("* from freedom where Country like '" + Country+"%'")
                if len(D3)>0:
                    D4=dict(D3[0].items()+D2.items())
                    scraperwiki.sqlite.save(['Country'],D4,table_name='freedom')
                
                else:
                    print 'Missing Country Name'+l[0][2]

main()
    


import scraperwiki
import urllib2
import lxml.etree
from lxml.html import tostring, fromstring

def main():
    url="http://www.freedomhouse.org/sites/default/files/Freedom%20OnThe%20Net_Full%20Report.pdf"
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    
    goodpages=[27,28,29]

    rootdata=lxml.etree.fromstring(xmldata)
    pages = list(rootdata)

    page=pages[23]
    alltext=getText(page)
    dict1(alltext)
    for i in goodpages:
        page=pages[i]
        alltext=getText(page)
        dict2(alltext)
    
        pagenumbers=[30,36,47,53, 57, 61, 65, 72, 78, 82, 87, 97, 102, 108]
        Country=['Brazil', 'China', 'Cuba', 'Egypt', 'Estonia', 'Georgia', 'India', 'Iran', 'Kenya', 'Malaysia','Russia','Tunisia', 'Turkey', 'UK']
    for i in range(len(pagenumbers)):
        page=pages[pagenumbers[i]]
        alltext=getText(page)
        PageInfo(alltext, Country[i])
    

def getText(page):

    alltext=[]
    
    for node in page.findall("text"):
        bold=node.find("b") 
        if not bold is None:
            text2=bold.text
        else:
            text2=node.text
        top=node.attrib["top"]
        left = node.attrib["left"]
        if text2 != ' ' and text2 is not None and text2.strip()!='Africa':
            if text2.strip()== 'South':
                text2= 'South Africa'
                top='343'
            alltext.append([top, left, text2])
    return alltext


def dict1(alltext):
    D={}
    for data in alltext:
        if data[0] in D:
            row=D[data[0]]
            row.append(data)
            D[data[0]]=row
        else:
            D[data[0]]=[data]

    headers =['Country', 'Freedom Status', 'Freedom Total', 'A Subtota','B Subtotal', 'S Subtotal']
    for top in D:
        D2={} 
        l= D[top]
        if len(l)==6:
            for i in range (len(l)):
                D2[headers[i]]=str(l[i][2])
            scraperwiki.sqlite.save(['Country'],D2,table_name='freedom')

                


def dict2(alltext):
    D={}

    for data in alltext:
        if data[0] in D:
            row=D[data[0]]
            row.append(data)
            D[data[0]]=row
        else:
            D[data[0]]=[data]

    headers =['Country','b','c','Freedom of the Press Total', 'Freedom of the Press Status']
    for top in D:
        D2={}
        l= D[top]
        if len(l)==5:
            for i in [3,4]:
                D2[headers[i]]=l[i][2]
            D3=scraperwiki.sqlite.select("* from freedom where Country like '" + l[0][2].strip()+"%'")
            if len(D3)>0:
                D4=dict(D3[0].items()+D2.items())
                scraperwiki.sqlite.save(['Country'],D4,table_name='freedom')
                
            else:
                print 'Missing Country Name'+l[0][2]




def PageInfo(alltext, Country):
    D={}
    print alltext
    for data in alltext:
        if data[1] in D:
            row=D[data[1]]
            row.append(data)
            D[data[1]]=row
        else:
            D[data[1]]=[data]
    for left in D:
        l= D[left]
        if left=='445':
            for e in l:
                D2={}
                [key, data]=e[2].split(':')
                key=str(key).replace('/', '-').replace('(', '-').replace(')','-').replace('.','-')
                data=str(data)
                D2[key]=data
                D3=scraperwiki.sqlite.select("* from freedom where Country like '" + Country+"%'")
                if len(D3)>0:
                    D4=dict(D3[0].items()+D2.items())
                    scraperwiki.sqlite.save(['Country'],D4,table_name='freedom')
                
                else:
                    print 'Missing Country Name'+l[0][2]

main()
    


