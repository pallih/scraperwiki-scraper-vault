import scraperwiki

scraperwiki.sqlite.attach("test123_3", "src")           
data = scraperwiki.sqlite.execute("select * from src.swdata")    
mylist = []
for row in data['data']:
    try:
        mydata = dict()
        mydata['panel_url'] = str(row[0]).strip().replace("\r","").replace("\n","")
        if mydata['panel_url'].find("../") != -1:
            mydata['panel_url'] = "http://www.posharp.com/" + str(mydata['panel_url'])[3:]
        else:
            mydata['panel_url'] = "http://www.posharp.com/photovoltaic/" + str(mydata['panel_url'])
        mydata['power'] = str(row[1]).strip().replace("\r","").replace("\n","")
        mydata['Voc'] = str(row[2]).strip().replace("\r","").replace("\n","")
        mydata['company_url'] = str(row[3]).strip().replace("\r","").replace("\n","")
        if mydata['company_url'].find("../") != -1:
            mydata['company_url'] = "http://www.posharp.com/" + str(mydata['company_url'])[3:]
        else:
            mydata['company_url'] = "http://www.posharp.com" + str(mydata['company_url'])
        mydata['company'] = str(row[4]).strip().replace("\r","").replace("\n","")
        mydata['Imp'] = str(row[5]).strip().replace("\r","").replace("\n","")
        mydata['Vmp'] = str(row[6]).strip().replace("\r","").replace("\n","")
        mydata['Isc'] = str(row[7]).strip().replace("\r","").replace("\n","")
        mydata['eff'] = str(row[8]).strip().replace("\r","").replace("\n","")
        mydata['panel'] = str(row[9]).strip().replace("\r","").replace("\n","")
        mylist.append(mydata)
    except:
        print "Skipped one..."
        continue

scraperwiki.sqlite.save(unique_keys=["panel_url"], data=mylist)
scraperwiki.sqlite.commit()