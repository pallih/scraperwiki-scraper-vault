# Blank Python
import scraperwiki
import string
from pyquery import PyQuery as pq
from lxml import etree
import urllib
base = 'http://www.liberliber.it/biblioteca/'

class LLParser:
    exception_authors = ("Andrea : da Barberino","Bernardino : da Siena <santo>","Caterina : da Siena <santa>","Cielo : d'Alcamo","Cronica : vita di Cola di Rienzo","Francesco : d'Assisi <santo>","Leonardo : da Vinci","Erasmus : Roterodamus","Fiore di leggende : cantari antichi editi e ordinati da Ezio Levi, serie I (cantari leggendari)","Folgore : da San Gimignano")
    exception_authors = ("Fiore di leggende : cantari antichi editi e ordinati da Ezio Levi, serie I (cantari leggendari)","")
    name_author = None
    lastname_author = None
    letter = None
    idb = -1
    def parsebook(self,b):
        data = {}
        book = str(b)
        idb = -1
        if (book.find('<!-- InstanceBeginEditable name="titolo" -->')) > -1:
            book = book.replace('<td class="testo_grande"><!-- InstanceBeginEditable name="titolo" -->','')
            book = book.replace('<!-- InstanceEndEditable --></td>\n','')
            self.idb += 1
            data = { 
                'id' : self.idb,
                'name_author' : self.name_author,
                'lastname_author' : self.lastname_author,
                'book' : book
            } 
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
 
    def chkauthorsexp(self,a):
        r = True
        for i in self.exception_authors:
            if (a == i):
                r = False
                self.lastname_author = a
                break
        return r
    
    def parseauthors(self,u):
        v = u.find("a")
        author = v.html()
        if author != None:
            print " -> %s" % author
            if (self.chkauthorsexp(author)):
                if (author.find(':')) > -1:
                    parsename= author.split(':')
                    if (author.find(',')) > -1:
                        self.name_author = parsename[0].split(",")[1]
                        self.lastname_author = parsename[1] + parsename[0].split(",")[0]
                    else:
                        self.name_author = parsename[0]
                        self.lastname_author = parsename[1]
                else:
                    if (author.find(',')) > -1:
                        self.name_author = author.split(",")[1]
                        self.lastname_author = author.split(",")[0]                
                    else:
                        self.name_author = ""
                        self.lastname_author = author
            bookurl = base + self.letter + "/" + str(v.attr("href")).strip()
            authorpage = pq(url=bookurl)
            books = authorpage("td").filter(".contenuto_cornice_centro").find("table").find(".testo_grande").each(self.parsebook)
    
ll = LLParser()
for i in string.ascii_lowercase:
    print "search for letter: %s" % i
    u = base + i + '/index.htm'
    ll.letter = i
    d = pq(url=u)
    p = d("td").filter(".contenuto_cornice_centro").find("ul").find("li").each(ll.parseauthors)

#i = "a"
#u = base + i + '/index.htm'
#ll.letter = i
#d = pq(url=u)
#p = d("td").filter(".contenuto_cornice_centro").find("ul").find("li").each(ll.parseauthors)
# Blank Python
import scraperwiki
import string
from pyquery import PyQuery as pq
from lxml import etree
import urllib
base = 'http://www.liberliber.it/biblioteca/'

class LLParser:
    exception_authors = ("Andrea : da Barberino","Bernardino : da Siena <santo>","Caterina : da Siena <santa>","Cielo : d'Alcamo","Cronica : vita di Cola di Rienzo","Francesco : d'Assisi <santo>","Leonardo : da Vinci","Erasmus : Roterodamus","Fiore di leggende : cantari antichi editi e ordinati da Ezio Levi, serie I (cantari leggendari)","Folgore : da San Gimignano")
    exception_authors = ("Fiore di leggende : cantari antichi editi e ordinati da Ezio Levi, serie I (cantari leggendari)","")
    name_author = None
    lastname_author = None
    letter = None
    idb = -1
    def parsebook(self,b):
        data = {}
        book = str(b)
        idb = -1
        if (book.find('<!-- InstanceBeginEditable name="titolo" -->')) > -1:
            book = book.replace('<td class="testo_grande"><!-- InstanceBeginEditable name="titolo" -->','')
            book = book.replace('<!-- InstanceEndEditable --></td>\n','')
            self.idb += 1
            data = { 
                'id' : self.idb,
                'name_author' : self.name_author,
                'lastname_author' : self.lastname_author,
                'book' : book
            } 
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
 
    def chkauthorsexp(self,a):
        r = True
        for i in self.exception_authors:
            if (a == i):
                r = False
                self.lastname_author = a
                break
        return r
    
    def parseauthors(self,u):
        v = u.find("a")
        author = v.html()
        if author != None:
            print " -> %s" % author
            if (self.chkauthorsexp(author)):
                if (author.find(':')) > -1:
                    parsename= author.split(':')
                    if (author.find(',')) > -1:
                        self.name_author = parsename[0].split(",")[1]
                        self.lastname_author = parsename[1] + parsename[0].split(",")[0]
                    else:
                        self.name_author = parsename[0]
                        self.lastname_author = parsename[1]
                else:
                    if (author.find(',')) > -1:
                        self.name_author = author.split(",")[1]
                        self.lastname_author = author.split(",")[0]                
                    else:
                        self.name_author = ""
                        self.lastname_author = author
            bookurl = base + self.letter + "/" + str(v.attr("href")).strip()
            authorpage = pq(url=bookurl)
            books = authorpage("td").filter(".contenuto_cornice_centro").find("table").find(".testo_grande").each(self.parsebook)
    
ll = LLParser()
for i in string.ascii_lowercase:
    print "search for letter: %s" % i
    u = base + i + '/index.htm'
    ll.letter = i
    d = pq(url=u)
    p = d("td").filter(".contenuto_cornice_centro").find("ul").find("li").each(ll.parseauthors)

#i = "a"
#u = base + i + '/index.htm'
#ll.letter = i
#d = pq(url=u)
#p = d("td").filter(".contenuto_cornice_centro").find("ul").find("li").each(ll.parseauthors)
