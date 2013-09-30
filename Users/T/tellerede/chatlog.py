import urllib, urllib2, cookielib, hashlib, time, scraperwiki, re, random, socket, pickle, dateutil.parser
from BeautifulSoup import BeautifulSoup

def variables():
    url = 'https://www.kenderforum.org/'
    uname ='ppp' #raw_input('Enter your username: ')
    passwd = 'p' #raw_input('Enter your password: ')

    login(url, uname, passwd)

def login(url, uname, passwd):
    uuu = 'Jelsz' + chr(162)
    loginurl = url + '/login.php?do=login'
    md5 = hashlib.md5(passwd);md5 = md5.hexdigest()
    # Options for request
    opts = {
    'vb_login_md5password_utf': md5,
    'vb_login_md5password': md5,
    'do': 'login',
    'securitytoken': 'guest',
    's': '',
    'cookieuser': '1',
    'vb_login_password_hint': uuu,
    'vb_login_password':'',
    'vb_login_username': uname,
    }

    data = urllib.urlencode(opts)

    # Request header
    global headers
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20100101 Firefox/7.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-gb,en;q=0.5',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Connection': 'keep-alive',
    'Referer': loginurl
    }

    # Cookie Handling
    jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

    # Send Request
    opener.addheader = headers
    try:
        opener.open(loginurl, data)
    except urllib2.URLError, e:
        pass
        print e
        time.sleep(30)
    except socket.timeout, e:
        pass
        print e
        time.sleep(30)
    except urllib2.HTTPError, e:
        pass
        print e
        time.sleep(30)  
    except e:
        pass
        print "URL hiba"
        time.sleep(30)  
    
    # Get the last row's hash
    try:
        lasthh = scraperwiki.sqlite.select('Hash FROM swdata WHERE id = (SELECT MAX(id) FROM swdata)');
    except:
        print 'sql hiba: '
        lasth = '000'    
        pass
    else:
        if lasthh:
            #print lasthh
            lasth = lasthh[0]['Hash']
            print lasth
            #print scraperwiki.sqlite.select("Datum, Nev, Text, Hash from swdata WHERE Hash=?",lasth)
        else:
            print "Nincs lasth"
            lasth = '000'
    
    
    # Define some variables    
    pagenum = 0
    oldal = 1
    oldalossz = 0
    vege = 0

    thash = []
    tnev = []
    tdatum = []
    tszoveg = []
    tdateformat = []

    while (oldal != oldalossz) and (vege != 1):
      pagenum=pagenum+1

      archiveurl = 'https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&channel_id=0&dlimit=-1&page=' + str(pagenum)

      e=1
      while e != 0:
        try:
            samplehtml = opener.open(archiveurl)
        except urllib2.URLError, e:
            pass
            print e
            time.sleep(30)
        except socket.timeout, e:
            pass
            print e
            time.sleep(30)
        except:
            pass
            e = 1
            time.sleep(30)
        else:
            e = 0

      wtf = samplehtml.read()
      soup = BeautifulSoup(wtf)
      szoveg = soup.findAll(id=re.compile('text.'))
      nev = soup.findAll(id=re.compile('uname.'))
      datum = soup.findAll(id=re.compile('date.'))
      oldalszamread = re.search('Oldal:\s(\d+)\s[r/]\s(\d+)', wtf)
      if oldalszamread:
          oldal = oldalszamread.group(1)
          oldalossz = oldalszamread.group(2)
          print "%s oldal / %s" % (oldal, oldalossz)
      else:
        print "Nem talált oldalszámot"
        vege = 1

      # Get links (shitty)
      kivett=[]
      for link in szoveg:
       if link.a <> None:
         kivett.append(link.a.get('href'))
       else:
         kivett.append('')

      for incu in range(0,len(szoveg)):
        nevtrimmed = nev[incu].text[4:len(nev[incu].text)-4] # Trim names from additional chars like <>
        # Hash
        sor = datum[incu].text + nevtrimmed + szoveg[incu].text
        hashedsor = hashlib.md5(sor.encode('utf-8'));hashedsor = hashedsor.hexdigest()

        formdatum = dateutil.parser.parse(datum[incu].text,dayfirst=True) #Parse dates
       
        #First row's hash into a temp variable
        #print "incu=%s oldal=%s" % (incu, oldal)
        
        '''if str(incu) == '0' and str(oldal) == '1':
            #lasthtemp = hashedsor
            try:
                scraperwiki.sqlite.save_var('lasth', pickle.dumps(hashedsor))
            except scraperwiki.sqlite.SqliteError ,e:     
                print str(e)
                pass
            else:
                print 'Az új lasth mentve : ', hashedsor
        '''    
        if hashedsor <> lasth:
            thash.append(hashedsor)
            tnev.append(nevtrimmed)
            tdatum.append(datum[incu].text)
            tdateformat.append(formdatum)
            tszoveg.append(szoveg[incu].text+kivett[incu])
        else:
            print hashedsor ,'=', lasth
            vege = 1
            break
    # Reverse the arrays to get incrementing timeline
    thash.reverse()
    tnev.reverse()
    tdatum.reverse()
    tszoveg.reverse()
    tdateformat.reverse()
    incu = -1
    # Save to DB
    for n in thash:
          incu +=1      
          err=0
          while err != 1:
              try:
                  scraperwiki.sqlite.save(unique_keys=["Hash"], data={"Hash":thash[incu], "Text":tszoveg[incu], "Nev":tnev[incu], "Datum":tdatum[incu], "Dateformat":tdateformat[incu]}, table_name="swdata")
              except scraperwiki.sqlite.SqliteError, e:     
                  print e
                  time.sleep(30)
                  err = 0
                  pass
              except:
                  time.sleep(30)
                  err = 0
                  pass
              else:
                  err = 1         

#lastrowid = scraperwiki.sqlite.select('MAX(rowid) FROM swdata')
#print lastrowid[0]['MAX(rowid)']
#null = 0
def makeclearupdb():
    #scraperwiki.sqlite.execute("alter table clearup rename to swdata")
    #scraperwiki.sqlite.execute("drop table if exists swvariables")
    #scraperwiki.sqlite.commit()
    '''
    e=''
    while e:
        try:
            scraperwiki.sqlite.execute("drop table if exists swdata")
        except e:
            print e
            time.sleep(30)
            pass
        else:
            e = ''
    scraperwiki.sqlite.commit()
    #scraperwiki.sqlite.execute("drop table if exists clearup")
    '''

def cleanup():
    data = scraperwiki.sqlite.select("Datum, Nev, Text, Hash from swdata")
    print len(data)
    for row in data[31727:]:
            print row
            dat = row["Datum"]
            datelett = dateutil.parser.parse(dat,dayfirst=True)
            '''
            if row["hash"] == None:
                sor = row["Datum"] + row["Nev"] + row["Text"]
                hashedsor = hashlib.md5(sor.encode('utf-8'));hashedsor = hashedsor.hexdigest()
                row["hash"] = hashedsor
            err=0
            while err != 1:
                try:
                    scraperwiki.sqlite.save(unique_keys=["Hash"], data={"Datum":row["Datum"],"Dateformat":datelett,"Nev":row["Nev"],"Hash":row["hash"],"Text":row["Text"]}, table_name="clearup")
                except scraperwiki.sqlite.SqliteError, e:     
                      print e
                      time.sleep(30)
                      err = 0
                      pass
                else:
                      err = 1
            '''
#cleanup()
#makeclearupdb()
variables()



import urllib, urllib2, cookielib, hashlib, time, scraperwiki, re, random, socket, pickle, dateutil.parser
from BeautifulSoup import BeautifulSoup

def variables():
    url = 'https://www.kenderforum.org/'
    uname ='ppp' #raw_input('Enter your username: ')
    passwd = 'p' #raw_input('Enter your password: ')

    login(url, uname, passwd)

def login(url, uname, passwd):
    uuu = 'Jelsz' + chr(162)
    loginurl = url + '/login.php?do=login'
    md5 = hashlib.md5(passwd);md5 = md5.hexdigest()
    # Options for request
    opts = {
    'vb_login_md5password_utf': md5,
    'vb_login_md5password': md5,
    'do': 'login',
    'securitytoken': 'guest',
    's': '',
    'cookieuser': '1',
    'vb_login_password_hint': uuu,
    'vb_login_password':'',
    'vb_login_username': uname,
    }

    data = urllib.urlencode(opts)

    # Request header
    global headers
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20100101 Firefox/7.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-gb,en;q=0.5',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Connection': 'keep-alive',
    'Referer': loginurl
    }

    # Cookie Handling
    jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

    # Send Request
    opener.addheader = headers
    try:
        opener.open(loginurl, data)
    except urllib2.URLError, e:
        pass
        print e
        time.sleep(30)
    except socket.timeout, e:
        pass
        print e
        time.sleep(30)
    except urllib2.HTTPError, e:
        pass
        print e
        time.sleep(30)  
    except e:
        pass
        print "URL hiba"
        time.sleep(30)  
    
    # Get the last row's hash
    try:
        lasthh = scraperwiki.sqlite.select('Hash FROM swdata WHERE id = (SELECT MAX(id) FROM swdata)');
    except:
        print 'sql hiba: '
        lasth = '000'    
        pass
    else:
        if lasthh:
            #print lasthh
            lasth = lasthh[0]['Hash']
            print lasth
            #print scraperwiki.sqlite.select("Datum, Nev, Text, Hash from swdata WHERE Hash=?",lasth)
        else:
            print "Nincs lasth"
            lasth = '000'
    
    
    # Define some variables    
    pagenum = 0
    oldal = 1
    oldalossz = 0
    vege = 0

    thash = []
    tnev = []
    tdatum = []
    tszoveg = []
    tdateformat = []

    while (oldal != oldalossz) and (vege != 1):
      pagenum=pagenum+1

      archiveurl = 'https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&channel_id=0&dlimit=-1&page=' + str(pagenum)

      e=1
      while e != 0:
        try:
            samplehtml = opener.open(archiveurl)
        except urllib2.URLError, e:
            pass
            print e
            time.sleep(30)
        except socket.timeout, e:
            pass
            print e
            time.sleep(30)
        except:
            pass
            e = 1
            time.sleep(30)
        else:
            e = 0

      wtf = samplehtml.read()
      soup = BeautifulSoup(wtf)
      szoveg = soup.findAll(id=re.compile('text.'))
      nev = soup.findAll(id=re.compile('uname.'))
      datum = soup.findAll(id=re.compile('date.'))
      oldalszamread = re.search('Oldal:\s(\d+)\s[r/]\s(\d+)', wtf)
      if oldalszamread:
          oldal = oldalszamread.group(1)
          oldalossz = oldalszamread.group(2)
          print "%s oldal / %s" % (oldal, oldalossz)
      else:
        print "Nem talált oldalszámot"
        vege = 1

      # Get links (shitty)
      kivett=[]
      for link in szoveg:
       if link.a <> None:
         kivett.append(link.a.get('href'))
       else:
         kivett.append('')

      for incu in range(0,len(szoveg)):
        nevtrimmed = nev[incu].text[4:len(nev[incu].text)-4] # Trim names from additional chars like <>
        # Hash
        sor = datum[incu].text + nevtrimmed + szoveg[incu].text
        hashedsor = hashlib.md5(sor.encode('utf-8'));hashedsor = hashedsor.hexdigest()

        formdatum = dateutil.parser.parse(datum[incu].text,dayfirst=True) #Parse dates
       
        #First row's hash into a temp variable
        #print "incu=%s oldal=%s" % (incu, oldal)
        
        '''if str(incu) == '0' and str(oldal) == '1':
            #lasthtemp = hashedsor
            try:
                scraperwiki.sqlite.save_var('lasth', pickle.dumps(hashedsor))
            except scraperwiki.sqlite.SqliteError ,e:     
                print str(e)
                pass
            else:
                print 'Az új lasth mentve : ', hashedsor
        '''    
        if hashedsor <> lasth:
            thash.append(hashedsor)
            tnev.append(nevtrimmed)
            tdatum.append(datum[incu].text)
            tdateformat.append(formdatum)
            tszoveg.append(szoveg[incu].text+kivett[incu])
        else:
            print hashedsor ,'=', lasth
            vege = 1
            break
    # Reverse the arrays to get incrementing timeline
    thash.reverse()
    tnev.reverse()
    tdatum.reverse()
    tszoveg.reverse()
    tdateformat.reverse()
    incu = -1
    # Save to DB
    for n in thash:
          incu +=1      
          err=0
          while err != 1:
              try:
                  scraperwiki.sqlite.save(unique_keys=["Hash"], data={"Hash":thash[incu], "Text":tszoveg[incu], "Nev":tnev[incu], "Datum":tdatum[incu], "Dateformat":tdateformat[incu]}, table_name="swdata")
              except scraperwiki.sqlite.SqliteError, e:     
                  print e
                  time.sleep(30)
                  err = 0
                  pass
              except:
                  time.sleep(30)
                  err = 0
                  pass
              else:
                  err = 1         

#lastrowid = scraperwiki.sqlite.select('MAX(rowid) FROM swdata')
#print lastrowid[0]['MAX(rowid)']
#null = 0
def makeclearupdb():
    #scraperwiki.sqlite.execute("alter table clearup rename to swdata")
    #scraperwiki.sqlite.execute("drop table if exists swvariables")
    #scraperwiki.sqlite.commit()
    '''
    e=''
    while e:
        try:
            scraperwiki.sqlite.execute("drop table if exists swdata")
        except e:
            print e
            time.sleep(30)
            pass
        else:
            e = ''
    scraperwiki.sqlite.commit()
    #scraperwiki.sqlite.execute("drop table if exists clearup")
    '''

def cleanup():
    data = scraperwiki.sqlite.select("Datum, Nev, Text, Hash from swdata")
    print len(data)
    for row in data[31727:]:
            print row
            dat = row["Datum"]
            datelett = dateutil.parser.parse(dat,dayfirst=True)
            '''
            if row["hash"] == None:
                sor = row["Datum"] + row["Nev"] + row["Text"]
                hashedsor = hashlib.md5(sor.encode('utf-8'));hashedsor = hashedsor.hexdigest()
                row["hash"] = hashedsor
            err=0
            while err != 1:
                try:
                    scraperwiki.sqlite.save(unique_keys=["Hash"], data={"Datum":row["Datum"],"Dateformat":datelett,"Nev":row["Nev"],"Hash":row["hash"],"Text":row["Text"]}, table_name="clearup")
                except scraperwiki.sqlite.SqliteError, e:     
                      print e
                      time.sleep(30)
                      err = 0
                      pass
                else:
                      err = 1
            '''
#cleanup()
#makeclearupdb()
variables()



