###############################################################################
# Eyjan Kommentarar - allir skradir kommentarar a eyjan.is
###############################################################################

import scraperwiki, urllib2, re, urllib, json, time
from BeautifulSoup import BeautifulSoup, SoupStrainer



kommentari = {}


def scrape_notandi(userid):
    notandi_sed_adur = scraperwiki.metadata.get(userid)
    if notandi_sed_adur is not None:
        #print "Sleppum notanda (sed adur): " + userid
        return
    else:


    #if userid is None or userid in seen: 
#        print "Sed adur - sleppum: " + userid 
#        return
    #seen.add(userid)
    #print seen
        url= "http://i.eyjan.is/notandi/" + userid
        print "Saekjum notanda: " + url
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()
        fjoldi = soup.find('h2')
        fjoldi = fjoldi.string
        fjoldi = extract(fjoldi, "Umm&aelig;li (",")")

    
        rest = soup.findAll('div','column2')
        for n in rest:
            notandi = n.findNext('h3')
            nafn = notandi.string
            mynd = n.findNext ('img')
            mynd = mynd["src"]
            mynd = re.sub("\./","http://i.eyjan.is/",mynd)
            kommentari['nafn'] = nafn
            kommentari['userid'] = userid
            kommentari['url'] = url
            kommentari['kommentafjoldi'] = fjoldi
            kommentari['mynd'] = mynd
         
            scraperwiki.datastore.save(["userid"], kommentari)
            ### SOFA
            #time.sleep(0.2)    
        print "vistum notanda metatada: " + userid         
        scraperwiki.metadata.save(userid, '1')


def extract(text, sub1, sub2):
    """extract a substring between two substrings sub1 and sub2 in text"""
    return text.split(sub1)[-1].split(sub2)[0]

def scrape_frett(url):
    kommentari['from_url'] = url
    print "Saekjum frett: " + url
    html = scraperwiki.scrape(url)
    time.sleep(0.2)    

    ckey = extract(html, "window.cKey = ",";")
    ckey = re.sub("\'",'',ckey)
    ckey = urllib.quote(ckey,'&')
    kommentjsonurl = "http://i.eyjan.is/c/action.php?n=getcomments&key="+ckey+"&o=time-asc"
    #time.sleep(0.2)    

    kommentjson = scraperwiki.scrape(kommentjsonurl)
    kommentjson=kommentjson[1:-1]

    userid = set(re.findall("userid\":([\d+]+)",kommentjson))
    for n in userid:
        scrape_notandi(n)
    print "vistum frett metatada: " + url 
    scraperwiki.metadata.save(url,'1')




def scrape_manudur(url):
    manudur_sed_adur = scraperwiki.metadata.get(url)

    if manudur_sed_adur is not None:
        print "Sleppum manudi (sed adur): " + url
        return
    else:
        print "****** Saekjum manud: " + url
    
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()
    
        tr = soup.findAll('tr') 
        for tr in tr:
 
            tengill = tr.findNext('a', href = re.compile(r".*comments.*"))
            kommentafjoldi = tengill.text
           
            if kommentafjoldi != "0":
                tengill = tengill['href']
                tengill = re.sub("#comments","",tengill)
                frett_sed_adur = scraperwiki.metadata.get(tengill)
                if frett_sed_adur is not None:
                    print "Sleppum frett (sed adur): " + tengill
                    continue
                else:
                #frett_seen.add(tengill)
                    
                    scrape_frett(tengill)
            else:
                print "Sleppum frett - engin komment: " + tengill['href']
    
    #Thegar allir frettatenglar bunir - vista manudinn sem metadata
    print "Vistum manudinn sem metatadata og done: " + url
    scraperwiki.metadata.save(url,'1')

def start(url):
    #starting_url = 'http://eyjan.is/frettir/sarpur/'
    html = scraperwiki.scrape(url)
    print html
    soup = BeautifulSoup(html)
    soup.prettify()


    manudir = soup.findAll('a', href = re.compile(r".*mnth.*"))
    for a in manudir:
        manadar_tengill = a['href']
        if re.match(r"http://eyjan.is.*", manadar_tengill, re.VERBOSE): 
            manadar_tengill = manadar_tengill
        else:
            manadar_tengill = "http://eyjan.is/frettir/sarpur/" + manadar_tengill
    
        print "Saekjum: " + manadar_tengill

        scrape_manudur(manadar_tengill)



#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=5&yr=2010') #- DONE
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=6&yr=2010') #- DONE
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=7&yr=2010') # DONE
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=8&yr=2010') # - Tharf ad keyra aftur - endudum 11.8
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=9&yr=2010') 
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=10&yr=2010') 
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=11&yr=2010') 
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=12&yr=2010') 
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=1&yr=2011') 
scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=2&yr=2011') 







#start('http://eyjan.is/frettir/sarpur/')###############################################################################
# Eyjan Kommentarar - allir skradir kommentarar a eyjan.is
###############################################################################

import scraperwiki, urllib2, re, urllib, json, time
from BeautifulSoup import BeautifulSoup, SoupStrainer



kommentari = {}


def scrape_notandi(userid):
    notandi_sed_adur = scraperwiki.metadata.get(userid)
    if notandi_sed_adur is not None:
        #print "Sleppum notanda (sed adur): " + userid
        return
    else:


    #if userid is None or userid in seen: 
#        print "Sed adur - sleppum: " + userid 
#        return
    #seen.add(userid)
    #print seen
        url= "http://i.eyjan.is/notandi/" + userid
        print "Saekjum notanda: " + url
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()
        fjoldi = soup.find('h2')
        fjoldi = fjoldi.string
        fjoldi = extract(fjoldi, "Umm&aelig;li (",")")

    
        rest = soup.findAll('div','column2')
        for n in rest:
            notandi = n.findNext('h3')
            nafn = notandi.string
            mynd = n.findNext ('img')
            mynd = mynd["src"]
            mynd = re.sub("\./","http://i.eyjan.is/",mynd)
            kommentari['nafn'] = nafn
            kommentari['userid'] = userid
            kommentari['url'] = url
            kommentari['kommentafjoldi'] = fjoldi
            kommentari['mynd'] = mynd
         
            scraperwiki.datastore.save(["userid"], kommentari)
            ### SOFA
            #time.sleep(0.2)    
        print "vistum notanda metatada: " + userid         
        scraperwiki.metadata.save(userid, '1')


def extract(text, sub1, sub2):
    """extract a substring between two substrings sub1 and sub2 in text"""
    return text.split(sub1)[-1].split(sub2)[0]

def scrape_frett(url):
    kommentari['from_url'] = url
    print "Saekjum frett: " + url
    html = scraperwiki.scrape(url)
    time.sleep(0.2)    

    ckey = extract(html, "window.cKey = ",";")
    ckey = re.sub("\'",'',ckey)
    ckey = urllib.quote(ckey,'&')
    kommentjsonurl = "http://i.eyjan.is/c/action.php?n=getcomments&key="+ckey+"&o=time-asc"
    #time.sleep(0.2)    

    kommentjson = scraperwiki.scrape(kommentjsonurl)
    kommentjson=kommentjson[1:-1]

    userid = set(re.findall("userid\":([\d+]+)",kommentjson))
    for n in userid:
        scrape_notandi(n)
    print "vistum frett metatada: " + url 
    scraperwiki.metadata.save(url,'1')




def scrape_manudur(url):
    manudur_sed_adur = scraperwiki.metadata.get(url)

    if manudur_sed_adur is not None:
        print "Sleppum manudi (sed adur): " + url
        return
    else:
        print "****** Saekjum manud: " + url
    
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()
    
        tr = soup.findAll('tr') 
        for tr in tr:
 
            tengill = tr.findNext('a', href = re.compile(r".*comments.*"))
            kommentafjoldi = tengill.text
           
            if kommentafjoldi != "0":
                tengill = tengill['href']
                tengill = re.sub("#comments","",tengill)
                frett_sed_adur = scraperwiki.metadata.get(tengill)
                if frett_sed_adur is not None:
                    print "Sleppum frett (sed adur): " + tengill
                    continue
                else:
                #frett_seen.add(tengill)
                    
                    scrape_frett(tengill)
            else:
                print "Sleppum frett - engin komment: " + tengill['href']
    
    #Thegar allir frettatenglar bunir - vista manudinn sem metadata
    print "Vistum manudinn sem metatadata og done: " + url
    scraperwiki.metadata.save(url,'1')

def start(url):
    #starting_url = 'http://eyjan.is/frettir/sarpur/'
    html = scraperwiki.scrape(url)
    print html
    soup = BeautifulSoup(html)
    soup.prettify()


    manudir = soup.findAll('a', href = re.compile(r".*mnth.*"))
    for a in manudir:
        manadar_tengill = a['href']
        if re.match(r"http://eyjan.is.*", manadar_tengill, re.VERBOSE): 
            manadar_tengill = manadar_tengill
        else:
            manadar_tengill = "http://eyjan.is/frettir/sarpur/" + manadar_tengill
    
        print "Saekjum: " + manadar_tengill

        scrape_manudur(manadar_tengill)



#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=5&yr=2010') #- DONE
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=6&yr=2010') #- DONE
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=7&yr=2010') # DONE
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=8&yr=2010') # - Tharf ad keyra aftur - endudum 11.8
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=9&yr=2010') 
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=10&yr=2010') 
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=11&yr=2010') 
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=12&yr=2010') 
#scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=1&yr=2011') 
scrape_manudur('http://eyjan.is/frettir/sarpur/?mnth=2&yr=2011') 







#start('http://eyjan.is/frettir/sarpur/')