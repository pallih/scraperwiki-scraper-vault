import StringIO
import scraperwiki
import urllib2
import string
import lxml.etree
import lxml.html
import lxml.cssselect
from bs4 import BeautifulSoup
import requests


try:
    scraperwiki.sqlite.execute("create table regions(name text, link text)")
    
except:
    print "Table probably already exists."

try:
    scraperwiki.sqlite.execute("create table hosps(name text, link text, suburb text, state text, sector text, a1rate text, a1moments text, a2rate text, a2moments text, a3rate text, a3moments text)")
    
except:
    print "Table probably already exists."

try:
    scraperwiki.sqlite.execute("create table bugs(name text, link text, state text, Year text,Cases text,Days text, Rate text, unique (link, Year))")
except:
    print "Bug table exists"

#try:
#    scraperwiki.sqlite.execute('DROP TABLE "bugs"')
#except:
#    print 'nuh uh'


def grabo(x):
    print 'value is',x
    print 'type is',type(x)
    print 'length is',len(x)
    try:
        print 'string is',str(x)
    except:
        print 'string does not work'
    try:
        print 'integer is',int(x)
    except:
        print 'integer does not work'
    try:
        print 'float is',float(x)
    except:
        print 'float does not work'
    print '-----------------------'

#first part gets all the hospital detail and puts it into the table

#first part of the first part gets all the regions for NSW,Vic,Qld,WA & SA (Tas/NT/ACT don't have subregions)

states = []#'nsw','vic','qld','wa','sa']

for state in states:
    #url = "http://www.myhospitals.gov.au/browse/"+state
    #data = urllib2.urlopen(url).read()
    #soup = BeautifulSoup(data)
    url = "http://175.107.141.155/Preview/browse/"+state
    page = requests.get(url,auth = ('embargo', 'q5j2SweF'),verify=False)
    g = StringIO.StringIO(page.content)
    soup = BeautifulSoup(g)
    regions = soup.findAll("a", { "class" : "link" })
    for a in regions:
        testr = scraperwiki.sqlite.execute("select * from regions where link = ?",a['href'])
        if len(testr['data']) < 1:
            data = {
              'name' : a.text,
              'link' : a['href'],
            }
            scraperwiki.sqlite.save(unique_keys=[],data=data,table_name='regions')

#second part of first part adds Tas/NT manually (ACT already added in NSW)
#tas = {
#  'name' : "Tasmania",
#  'link' : "/Preview/browse/tas/tasmania",
#}
#scraperwiki.sqlite.save(unique_keys=[],data=tas,table_name='regions')
#nt = {
#  'name' : "Northern Territory",
#  'link' : "/Preview/browse/nt",
#}
#scraperwiki.sqlite.save(unique_keys=[],data=nt,table_name='regions')

#part two - getting the names and links of hospitals
them = ["odd","even"]
allregs = scraperwiki.sqlite.select("* from regions where name = 'Northern Territory'")
for reg in allregs:
    oldpage = requests.get("http://google.com").content
    count = 1
    while True:
        if reg['name'] == "Northern Territory":
            url = "http://175.107.141.155" + reg['link']
        else:
            url = "http://175.107.141.155" + reg['link'] + "/name-asc/" + str(count)
        newpage = requests.get(url,auth = ('embargo', 'q5j2SweF'),verify=False).content
        data = StringIO.StringIO(newpage)      
        print 'LENGTHS old:',len(oldpage),'new:',len(newpage)
        if oldpage == newpage:
            print 'last page for',reg['name'],'is',(count-1)
            break
        oldpage = newpage
        soup = BeautifulSoup(data)
        for him in them:
            hosos = soup.findAll("tr", { "class" : him })
            for tr in hosos:
                scraperwiki.sqlite.save(unique_keys=["link"], data={
                  "link": tr.contents[1].a['href'],
                  "name": tr.contents[1].a.text,
                  "suburb": tr.contents[3].text,
                  "state": tr.contents[5].text,
                  "sector": tr.contents[7].text
                },table_name='hosps')
        count += 1

#part three - getting the hygiene data for the hospitals

years = ["2011-12","2010-11"]
allhosps = scraperwiki.sqlite.select("* from hosps where state = 'NT'")
for h in allhosps:
    if scraperwiki.sqlite.select("* from bugs where link = ?",(h['link'])) == []:
        url = "http://175.107.141.155" + h['link'] + "/safety-and-quality/sab"
        page = requests.get(url,auth = ('embargo', 'q5j2SweF'),verify=False)
        g = StringIO.StringIO(page.content)
        soup = BeautifulSoup(g)
        for y in years:
            comp = soup.find(text=y)
            if comp == None:
                #print 'No SAB data in',y,'for',h['name']
                data = {"name":h['name'],"link":h['link'],"state":h['state'],"Year":"No SAB data available","Cases":"No SAB data available","Days":"No SAB data available","Rate":"No SAB data available"}
                scraperwiki.sqlite.save(unique_keys=["link","Year"],data=data,table_name='bugs')
            else:
                try:
                    data = {"name":h['name'],"link":h['link'],"state":h['state'],"Year":y,"Cases":comp.parent.parent.contents[3].contents[0],"Days":comp.parent.parent.contents[5].contents[0],"Rate":comp.parent.parent.contents[7].contents[0]}
                    scraperwiki.sqlite.save(unique_keys=["link","Year"],data=data,table_name='bugs')
                except:
                    print 'data in different format for',h['name']
                    data = {"name":h['name'],"link":h['link'],"state":h['state'],"Year":"No SAB data available","Cases":"No SAB data available","Days":"No SAB data available","Rate":"No SAB data available"}
                    scraperwiki.sqlite.save(unique_keys=["link","Year"],data=data,table_name='bugs')
    else:
        print h['name'],'is already in bugs'
        







#for h in allhosps:
#    #this variable at the start is for pages with no list items in the hand hygiene sector
#    nolist = 0
#    showem = {}
#    showem['Audit period 2, ending June 2012'] = ["No hygiene data available","No hygiene data available"]
#    showem['Audit period 1, ending February 2012'] = ["No hygiene data available","No hygiene data available"]
#    showem['Audit period 3, ending October 2011'] = ["No hygiene data available","No hygiene data available"]
#    url = "http://www.myhospitals.gov.au" + h['link'] + "/safety-and-quality/hand-hygiene"
#    req = urllib2.Request(url)
#    try:
#        data = urllib2.urlopen(url).read()
#    except urllib2.HTTPError as e:
#        pass
#        #print 'NO PAGE! for',h['link']
#    else:
#        soup = BeautifulSoup(data)
#       for him in them:
#            audits = soup.findAll("tr", { "class" : him })
#            #this part grabs the data from the top line, for pages that don't include any <tr> elements
#            if audits == []:
#                nolist += 1
#                if nolist == 2:
#                    oneline = soup.findAll("p", { "style" : 'margin-bottom:0'})
#                    if oneline != []:
#                        check = oneline[0].text.find("For Audit period 2, ending June 2012")
#                        if check != -1:
#                            percpos = oneline[0].text.find("%")
#                            spacepos = oneline[0].text.find(" ",percpos-6)
#                            try:
#                                rat = float(oneline[0].text[spacepos:percpos])/100
#                            except:
#                                print 'CANNOT TURN ONELINE PERCENT INTO FLOAT'
#                            x = len(oneline[0].text)
#                            mhandpos = oneline[0].text.rfind("hand")
#                            mbspacepos = oneline[0].text.rfind(" ",0,mhandpos-1)
#                            try:
#                                momo = int(oneline[0].text[mbspacepos:mhandpos])
#                            except:
#                                print 'CANNOT TURN ONELINE MOMENT INTO INTEGER'
#                            showem['Audit period 2, ending June 2012'] = [rat,momo]
#                        else:
#                            print 'THE PERIOD IN ONELINE IS NOT For Audit period 2, ending June 2012'
#                    else:
#                        print 'THERE IS NO ONELINE FOO'
#            for tr in audits:
#                try:
#                    period = tr.contents[1].text
#                except:
#                    print 'FIRST UP,cannot print tr.contents[1].text - aka the period - for',h['name']
#                try:
#                    #print tr.contents[3].text
#                    percent = float(tr.contents[3].text.strip('%'))/100
#                    
#                    try:
#                        moments = tr.contents[5].text
#                        percent = tr.contents[3].text
#                        showem[tr.contents[1].text]= [percent,moments]
#                        #print showem[tr.contents[1].text]
#                    except:
#                        print 'I CANNOT PRINT tr.contents[5].text for',h['name'],'for',tr.contents[1].text
#                except:
#                    #print 'cannot print float(tr.contents[3].text.strip("%")/100) for',h['name'],'for the period',period
#                    try:
#                        if tr.contents[3].text == "Data are not available for this hospital":
#                            showem[tr.contents[1].text]= [tr.contents[3].text,tr.contents[3].text]
#                        elif tr.contents[3].text == "Data are not reported for this hospital on MyHospitals":
#                            showem[tr.contents[1].text]= [tr.contents[3].text,tr.contents[3].text]
#                        elif tr.contents[3].text == "Data are not reported for this type of hospital on MyHospitals":
#                            showem[tr.contents[1].text]= [tr.contents[3].text,tr.contents[3].text]
#                        elif tr.contents[3].text == "This hospital had a very small number of 'moments' so no data are shown":
#                            showem[tr.contents[1].text]= [tr.contents[3].text,tr.contents[3].text]
#                        else:
#                            print 'cannot print an accepted field for',h['name'],'for the period',tr.contents[1].text
#                            showem[tr.contents[1].text]= ["Data not scraped as this page is in a different format","Data not scraped as this page is in a different format"]
#                    except:
#                        print 'cannot even print tr.contents[3].text for',h['name']
#                        print tr.contents[3].text
#                        
#    
#    data={
#          "link": h['link'],
#          "name": h['name'],
#          "suburb": h['suburb'],
#          "state": h['state'],
#          "sector": h['sector'],
#          "a1rate": showem['Audit period 3, ending October 2011'][0],
#          "a1moments": showem['Audit period 3, ending October 2011'][1],
#          "a2rate": showem['Audit period 1, ending February 2012'][0],
#          "a2moments": showem['Audit period 1, ending February 2012'][1],
#          "a3rate": showem['Audit period 2, ending June 2012'][0],
#          "a3moments": showem['Audit period 2, ending June 2012'][1],
#    }                  
#    scraperwiki.sqlite.save(unique_keys=["link"], data=data,table_name='hosps')
#    #print data


