import mechanize
import lxml.html
import scraperwiki
class scraper():
    
    def __init__(self):
        self.br=mechanize.Browser()
        self.br1=mechanize.Browser()
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        self.br1.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        
    def scrape(self):
        self.id=0;
        nf=1
        br=self.br
        url="http://h.bizdirlib.com/m/taxonomy/term/47192?page=22000"
        while nf:
            
            try:
                br.open(url,timeout=30.0)
                ll=lxml.html.fromstring(br.response().read())
                next=ll.cssselect("li[class='pager-next'] a")[0]
                data=ll.cssselect("h2 a")
                
                while nf:
                    print "Stranica:"+br.geturl()
                    for links in data:
                        self.br1.open("http://h.bizdirlib.com"+links.attrib['href'],timeout=30.0)
                        lll=lxml.html.fromstring(self.br1.response().read())
                        Company_Name="n/a"
                        City="n/a"
                        State="n/a"
                        ZIP_Code="n/a"
                        Telephone="n/a"
                        try:
                            Company_Name=lll.cssselect("span[itemprop='name']")[0].text
                        except: 
                            print "CErr"
                            Company_Name="n/a"
                        try:
                            City=lll.cssselect("span[itemprop='addressLocality'] a")[0].text
                        except:
                            print "CityErr"
                            City="n/a"
                        try:
                            State=lll.cssselect("span[itemprop='addressRegion'] a" )[0].text
                        except:
                            print "StErr"
                            State="n/a"
                        try:
                            ZIP_Code=lll.cssselect("span[itemprop='postalCode'] a")[0].text
                        except:
                            print "ZErr"
                            ZIP_Code='n/a'
                        try:
                            Telephone=lll.cssselect("span[itemprop='telephone']")[0].text
                        except:
                            print "TERR"
                            Telephone=n/a
                        self.save_data(Company_Name,City,State,ZIP_Code,Telephone)
                    try:
                        br.follow_link(text_regex='next')
                        url=br.geturl()
                        ll=lxml.html.fromstring(br.response().read())
                        data=ll.cssselect("h2 a")
                    except:
                        nf=0
            except:
                print "error"
                
    def save_data(self,Company_Name,City,State,ZIP_Code,Telephone):
        dicte={'id':self.id,'company_name':Company_Name,'city':City,'state': State,'zip_code':ZIP_Code,'telephone':Telephone}
        #print dict

        scraperwiki.sqlite.save(unique_keys=["id"],data=dicte)
        #scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "bbb":"Bye there"})

        self.id=self.id+1
        
    

a=scraper()
a.scrape()

# Blank Python

import mechanize
import lxml.html
import scraperwiki
class scraper():
    
    def __init__(self):
        self.br=mechanize.Browser()
        self.br1=mechanize.Browser()
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        self.br1.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        
    def scrape(self):
        self.id=0;
        nf=1
        br=self.br
        url="http://h.bizdirlib.com/m/taxonomy/term/47192?page=22000"
        while nf:
            
            try:
                br.open(url,timeout=30.0)
                ll=lxml.html.fromstring(br.response().read())
                next=ll.cssselect("li[class='pager-next'] a")[0]
                data=ll.cssselect("h2 a")
                
                while nf:
                    print "Stranica:"+br.geturl()
                    for links in data:
                        self.br1.open("http://h.bizdirlib.com"+links.attrib['href'],timeout=30.0)
                        lll=lxml.html.fromstring(self.br1.response().read())
                        Company_Name="n/a"
                        City="n/a"
                        State="n/a"
                        ZIP_Code="n/a"
                        Telephone="n/a"
                        try:
                            Company_Name=lll.cssselect("span[itemprop='name']")[0].text
                        except: 
                            print "CErr"
                            Company_Name="n/a"
                        try:
                            City=lll.cssselect("span[itemprop='addressLocality'] a")[0].text
                        except:
                            print "CityErr"
                            City="n/a"
                        try:
                            State=lll.cssselect("span[itemprop='addressRegion'] a" )[0].text
                        except:
                            print "StErr"
                            State="n/a"
                        try:
                            ZIP_Code=lll.cssselect("span[itemprop='postalCode'] a")[0].text
                        except:
                            print "ZErr"
                            ZIP_Code='n/a'
                        try:
                            Telephone=lll.cssselect("span[itemprop='telephone']")[0].text
                        except:
                            print "TERR"
                            Telephone=n/a
                        self.save_data(Company_Name,City,State,ZIP_Code,Telephone)
                    try:
                        br.follow_link(text_regex='next')
                        url=br.geturl()
                        ll=lxml.html.fromstring(br.response().read())
                        data=ll.cssselect("h2 a")
                    except:
                        nf=0
            except:
                print "error"
                
    def save_data(self,Company_Name,City,State,ZIP_Code,Telephone):
        dicte={'id':self.id,'company_name':Company_Name,'city':City,'state': State,'zip_code':ZIP_Code,'telephone':Telephone}
        #print dict

        scraperwiki.sqlite.save(unique_keys=["id"],data=dicte)
        #scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "bbb":"Bye there"})

        self.id=self.id+1
        
    

a=scraper()
a.scrape()

# Blank Python

