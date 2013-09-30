import scraperwiki
import urllib
import lxml.html           
from time import sleep

#Load the names from a separate database.
scraperwiki.sqlite.attach('south_dakota_lobbyists')
surnames=[row['last_name'] for row in scraperwiki.sqlite.select('distinct `last_name` from `splitnames` where `last_name` not in (select upper(`surname`) from `surnames_scraped`) limit 200;')]

#Create the surnames_scraped table
#scraperwiki.sqlite.save(['surname'],scraperwiki.sqlite.select('distinct `sname` as "surname" from `swdata`'),'surnames_scraped')

class ServerLimit(Exception):
    pass

print surnames[0:5]
url='http://bfm.sd.gov/ledger/employee.asp'

try:
  for surname in surnames:
    #try:
    #    q=scraperwiki.sqlite.select("* from swdata where upper(sname)=? limit 1", surname)
    #    if q:  
    #        print "Skipping surname: %s"%surname
    #        continue
    #except:
    #    print "select failed"
    #    pass

    data=urllib.urlencode({'cLast_Name':surname,
                           'cFirst_Name':'',
                           'cSubmit':'Display Employee',
                           'isSubmitted':'yes'})

    html=urllib.urlopen(url,data).read()
    print html
    root=lxml.html.fromstring(html)
    try:
        assert root.cssselect("tr")
    except AssertionError:
        raise ServerLimit("There are no table rows: start again from %s"%surname)
    for tr in root.cssselect("tr")[5:]: # 5 skips the first box.
        row={}
        tds = map(lxml.html.HtmlElement.text_content,tr.cssselect("td"))
        
        try: # pack into dictionary; failure implies no returns, but confirm anyway.
            (row['id'],row['sname'],row['fname'],row['mi'],row['agency'],row['title'],row['wage'],row['basis'])=map(unicode.strip, tds)
        except ValueError:
            assert 'complete' in tds[0]
            print "%s: no results"% surname
            continue

        try: # to convert wage to a number, but provide unmodified string on failure.
            row['wage']=float(row['wage'].replace('$','').replace(',',''))
        except:
            print "unable to convert wage"
        scraperwiki.sqlite.save(unique_keys=[], data=row)
        print row
    scraperwiki.sqlite.save(['surname'],{"surname":surname},'surnames_scraped')
except ServerLimit,e:
  print eimport scraperwiki
import urllib
import lxml.html           
from time import sleep

#Load the names from a separate database.
scraperwiki.sqlite.attach('south_dakota_lobbyists')
surnames=[row['last_name'] for row in scraperwiki.sqlite.select('distinct `last_name` from `splitnames` where `last_name` not in (select upper(`surname`) from `surnames_scraped`) limit 200;')]

#Create the surnames_scraped table
#scraperwiki.sqlite.save(['surname'],scraperwiki.sqlite.select('distinct `sname` as "surname" from `swdata`'),'surnames_scraped')

class ServerLimit(Exception):
    pass

print surnames[0:5]
url='http://bfm.sd.gov/ledger/employee.asp'

try:
  for surname in surnames:
    #try:
    #    q=scraperwiki.sqlite.select("* from swdata where upper(sname)=? limit 1", surname)
    #    if q:  
    #        print "Skipping surname: %s"%surname
    #        continue
    #except:
    #    print "select failed"
    #    pass

    data=urllib.urlencode({'cLast_Name':surname,
                           'cFirst_Name':'',
                           'cSubmit':'Display Employee',
                           'isSubmitted':'yes'})

    html=urllib.urlopen(url,data).read()
    print html
    root=lxml.html.fromstring(html)
    try:
        assert root.cssselect("tr")
    except AssertionError:
        raise ServerLimit("There are no table rows: start again from %s"%surname)
    for tr in root.cssselect("tr")[5:]: # 5 skips the first box.
        row={}
        tds = map(lxml.html.HtmlElement.text_content,tr.cssselect("td"))
        
        try: # pack into dictionary; failure implies no returns, but confirm anyway.
            (row['id'],row['sname'],row['fname'],row['mi'],row['agency'],row['title'],row['wage'],row['basis'])=map(unicode.strip, tds)
        except ValueError:
            assert 'complete' in tds[0]
            print "%s: no results"% surname
            continue

        try: # to convert wage to a number, but provide unmodified string on failure.
            row['wage']=float(row['wage'].replace('$','').replace(',',''))
        except:
            print "unable to convert wage"
        scraperwiki.sqlite.save(unique_keys=[], data=row)
        print row
    scraperwiki.sqlite.save(['surname'],{"surname":surname},'surnames_scraped')
except ServerLimit,e:
  print e