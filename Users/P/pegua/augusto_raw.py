import scraperwiki
import lxml.html

pre =  "/gazzette/index/download/id/"
site = "http://augusto.digitpa.gov.it"

all = set();

scraperwiki.sqlite.save_var("year_todo",1860)

#start year modified manually to overcome errors
for year in range(scraperwiki.sqlite.get_var("year_todo"),1947):
    scraperwiki.sqlite.save_var("year_todo",year)
    for month in range(1,13):
        for day in range(1,32):
            #addr = "http://augusto.digitpa.gov.it/#giorno=" + str(day) + "&mese=" + str(month) + "&anno=" + str(year)
            #Address obtained inspecting http requests
            addr = "http://augusto.digitpa.gov.it/gazzette/index/corpo-mese/anno/" + str(year) + "/mese/" + str(month) + "/giorno/" + str(day) +"/"
            print addr;
            html = scraperwiki.scrape(addr)
            #print html;
            root = lxml.html.fromstring(html);
            for el in root.cssselect("a"):
                ref = el.attrib['href']
                if ref[0:len(pre)] == pre:
                     #print ref
                     #all.add(ref);
                     complete_addr = site + ref
                     scraperwiki.sqlite.save(unique_keys=["complete_address"], data={"complete_address":complete_addr})           

#print all
for el in all:
    complete_addr = site + el
    scraperwiki.sqlite.save(unique_keys=["complete_address"], data={"complete_address":complete_addr})           