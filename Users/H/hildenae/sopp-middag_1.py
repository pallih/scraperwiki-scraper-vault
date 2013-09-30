# Blank Python

import scraperwiki
utils=scraperwiki.swimport('hildenae_utils')
import lxml.html
from lxml import etree

#scraperwiki.utils.httpresponseheader("Content-Type", 'text/plain; charset="utf-8"')

#scraperwiki.sqlite.attach("sopp-middag-view", "src")


def extractTable(root):
    for el in root.cssselect("div.content table.contentpaneopen table"):
        tableSource = lxml.html.tostring(el)
        if "Ukedag" in tableSource:
            return el        

def cleanup(table):
    etree.strip_tags(table,'span','strong','div', 'tbody')
    for tag in table.iter():
        for att in tag.attrib.keys():
            tag.attrib.pop(att)
        if tag.tag == "table": tag.set('border','1')
    return table;

def tds(td):
    tdstr = lxml.etree.tostring(td)
    cleaned = tdstr.replace('&#13;','').replace('&#160;', ' ').replace('/n', '').replace('</td>', '').replace('<td>', '').replace('<p>','').replace('<br />','<br>');
    cleaned2 = utils.removeDoubleSpaces(cleaned).replace('</p>','<br>').replace('<br><br>','<br>').replace('> ','>').replace(' <','<');
    if cleaned2.endswith("<br>"):
        r =cleaned2[:-4];
    else: r = cleaned2;
    return br2eller(r);

def br2eller(s):
    numbr = s.count('<br>')
    s = s.replace("<br>", ", ", numbr-1);
    return s.replace("<br>", ", eller ").replace('m/', "med ");

def tableToDict(ctable):
    names = ['header','Mandag','Tirsdag','Onsdag','Torsdag', 'Fredag']
    d = {}
    trs = ctable.cssselect("tr");
    td = 0;
    for tr in range(0,6):
        d[names[tr]] = [tds(trs[tr][td]),tds(trs[tr][td+1]),tds(trs[tr][td+2])]
    return d;

def printWeek(week):
    #print week
    for weekday in 'Mandag','Tirsdag','Onsdag','Torsdag', 'Fredag':
        for kantine in 1,2:
            week[weekday][kantine] = week[weekday][kantine].capitalize()
        f = lxml.html.fromstring(';'.join(week[weekday][1:3]))
        print weekday + ';' + f.text

#middag="http://sopp.no/index.php?option=com_content&view=article&id=56&Itemid=67"
#data = ('2013-17','2013-12-3','2013-13-3','2013-14-1','2013-15-1','2013-16')
#print "<html><body>"

#for week in data:
#    html = utils.findInCache(middag + "#" +  week, tableName="src.__cache", verbose=False)
#    
#    root = lxml.html.fromstring(html)
#    
#    table = extractTable(root)
#    
#    ctable = cleanup(table)
#    
#    d = tableToDict(table);
    #print d
#    printWeek(d);
    #print lxml.html.tostring(ctable)

#print "</body></html>"
# Blank Python

import scraperwiki
utils=scraperwiki.swimport('hildenae_utils')
import lxml.html
from lxml import etree

#scraperwiki.utils.httpresponseheader("Content-Type", 'text/plain; charset="utf-8"')

#scraperwiki.sqlite.attach("sopp-middag-view", "src")


def extractTable(root):
    for el in root.cssselect("div.content table.contentpaneopen table"):
        tableSource = lxml.html.tostring(el)
        if "Ukedag" in tableSource:
            return el        

def cleanup(table):
    etree.strip_tags(table,'span','strong','div', 'tbody')
    for tag in table.iter():
        for att in tag.attrib.keys():
            tag.attrib.pop(att)
        if tag.tag == "table": tag.set('border','1')
    return table;

def tds(td):
    tdstr = lxml.etree.tostring(td)
    cleaned = tdstr.replace('&#13;','').replace('&#160;', ' ').replace('/n', '').replace('</td>', '').replace('<td>', '').replace('<p>','').replace('<br />','<br>');
    cleaned2 = utils.removeDoubleSpaces(cleaned).replace('</p>','<br>').replace('<br><br>','<br>').replace('> ','>').replace(' <','<');
    if cleaned2.endswith("<br>"):
        r =cleaned2[:-4];
    else: r = cleaned2;
    return br2eller(r);

def br2eller(s):
    numbr = s.count('<br>')
    s = s.replace("<br>", ", ", numbr-1);
    return s.replace("<br>", ", eller ").replace('m/', "med ");

def tableToDict(ctable):
    names = ['header','Mandag','Tirsdag','Onsdag','Torsdag', 'Fredag']
    d = {}
    trs = ctable.cssselect("tr");
    td = 0;
    for tr in range(0,6):
        d[names[tr]] = [tds(trs[tr][td]),tds(trs[tr][td+1]),tds(trs[tr][td+2])]
    return d;

def printWeek(week):
    #print week
    for weekday in 'Mandag','Tirsdag','Onsdag','Torsdag', 'Fredag':
        for kantine in 1,2:
            week[weekday][kantine] = week[weekday][kantine].capitalize()
        f = lxml.html.fromstring(';'.join(week[weekday][1:3]))
        print weekday + ';' + f.text

#middag="http://sopp.no/index.php?option=com_content&view=article&id=56&Itemid=67"
#data = ('2013-17','2013-12-3','2013-13-3','2013-14-1','2013-15-1','2013-16')
#print "<html><body>"

#for week in data:
#    html = utils.findInCache(middag + "#" +  week, tableName="src.__cache", verbose=False)
#    
#    root = lxml.html.fromstring(html)
#    
#    table = extractTable(root)
#    
#    ctable = cleanup(table)
#    
#    d = tableToDict(table);
    #print d
#    printWeek(d);
    #print lxml.html.tostring(ctable)

#print "</body></html>"
